#!/usr/bin/env python3
"""Lokale CI fuer Aurum II.

  python tools/ci.py verify-frozen   # Originale unveraendert (git-Tag), Expected-SHA-Listen, Holdout-Manifest
  python tools/ci.py portable        # portable/ == mechanische Transformation der Originale
  python tools/ci.py tests           # 34 eingefrorene Tests (portable) + Repo-Tests
  python tools/ci.py repro [--fast]  # 4 Reproduktionen (DT, XRP, BTC Stufe B, Stufe 2; --fast ohne Stufe 2)
  python tools/ci.py all [--fast]
Exit-Code != 0 bei jedem Fehler.
"""
import functools, hashlib, json, math, os, re, shutil, subprocess, sys, time
print = functools.partial(print, flush=True)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = "original-2026-10-01"
PY = sys.executable
ROOT = os.path.abspath(os.environ.get("AURUM_ROOT") or os.path.join(REPO, "build", "root"))
EXPECTED_TESTS = 34


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def env():
    e = dict(os.environ, AURUM_ROOT=ROOT, PYTHONDONTWRITEBYTECODE="1")
    e.pop("AURUM_VALIDATION", None)
    e["PYTHONPATH"] = os.pathsep.join(os.path.join(ROOT, d) for d in ("pylib", "yamato", "rtc", "micro", "dt"))
    return e


def guard():
    if os.path.exists("/home/claude"):
        sys.exit("FEHLER: /home/claude existiert. Die eingefrorenen Libraries (rlib, dtlib) setzen diesen Pfad an den Anfang von sys.path "
                 "und wuerden den Arbeitsbereich ueberschatten. Bitte entfernen oder umbenennen.")


def stage():
    subprocess.run([PY, os.path.join(REPO, "tools", "stage_root.py")], check=True, env=dict(os.environ, AURUM_ROOT=ROOT))


# ------------------------------------------------------------------ verify-frozen
def verify_frozen():
    fails = 0
    r = subprocess.run(["git", "-C", REPO, "diff", "--name-status", TAG], capture_output=True, text=True, check=True)
    changed = [l for l in r.stdout.splitlines() if l and l[0] in "MDRT"]
    tagged = set(subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", TAG], capture_output=True, text=True, check=True).stdout.split())
    bad = [l for l in changed if l.split("\t")[-1] in tagged or l[0] in "DR"]
    print(f"[frozen] Originaldateien seit {TAG} veraendert/geloescht: {len(bad)} (von {len(tagged)})")
    for l in bad:
        print("   ", l)
    fails += len(bad)
    allow = {}
    for line in open(os.path.join(REPO, "tools", "frozen_allowlist.txt"), encoding="utf-8"):
        if line.strip() and not line.startswith("#"):
            f, p, why = line.rstrip("\n").split("|", 2); allow[(f, p)] = why
    lists = sorted(os.path.relpath(os.path.join(d, f), REPO) for d, _, fs in os.walk(REPO)
                   if "/build" not in d and "/.git" not in d and "/data" not in d for f in fs if f.endswith("expected_shas.txt"))
    for lf in lists:
        ok = dev = 0
        for line in open(os.path.join(REPO, lf), encoding="utf-8"):
            if not line.strip():
                continue
            h, p = line.split(None, 1); p = p.strip()
            fp = os.path.join(REPO, p)
            if os.path.exists(fp) and sha(fp) == h:
                ok += 1
            elif (lf, p) in allow or ("*", p) in allow:
                dev += 1
            else:
                print(f"    FEHLER {lf}: {p}"); fails += 1
        print(f"[frozen] {lf}: {ok} OK, {dev} begruendete Abweichung(en)")
    m = json.load(open(os.path.join(REPO, "02_daten/holdout/holdout_manifest_v1.1.json")))
    n = 0
    for k, v in m["files"].items():
        for part in ("discovery", "validation"):
            p = os.path.join(REPO, "02_daten/holdout", v[part]["path"]); n += 1
            if sha(p) != v[part]["sha256"]:
                print(f"    FEHLER Holdout {v[part]['path']}"); fails += 1
    print(f"[frozen] Holdout-Manifest v1.1: {n} Dateien geprueft (nur Pruefsumme, kein Laden)")
    return fails


def portable():
    return subprocess.run([PY, os.path.join(REPO, "tools", "make_portable.py"), "--check"]).returncode


# ------------------------------------------------------------------ tests
SUITES = [("yamato", ["tests/test_ylib_portable.py"]), ("rtc", ["tests/test_rlib_portable.py"]),
          ("micro", ["tests/test_mlib_portable.py", "tests/test_simulate_portable.py"]), ("dt", ["tests/test_dtlib_portable.py"])]


def run_pytest(cwd, files, e):
    r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", *files], cwd=cwd, env=e, capture_output=True, text=True)
    m = re.search(r"(\d+) passed", r.stdout); f = re.search(r"(\d+) (failed|error)", r.stdout)
    return r.returncode, int(m.group(1)) if m else 0, r.stdout


def tests():
    guard(); stage(); e = env(); total = 0; fails = 0
    for d, files in SUITES:
        rc, n, out = run_pytest(os.path.join(ROOT, d), files, e); total += n
        print(f"[tests] {d}: {n} bestanden, rc={rc}")
        if rc:
            print(out[-3000:]); fails += 1
    print(f"[tests] eingefrorene Suites total: {total}/{EXPECTED_TESTS}")
    if total != EXPECTED_TESTS:
        fails += 1
    rc, n, out = run_pytest(REPO, ["tests"], dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    print(f"[tests] Repo-Tests (tests/): {n} bestanden, rc={rc}")
    if rc:
        print(out[-3000:]); fails += 1
    return fails


# ------------------------------------------------------------------ repro
def expected(listfile, prefix):
    d = {}
    for line in open(os.path.join(REPO, listfile), encoding="utf-8"):
        if line.strip():
            h, p = line.split(None, 1); p = p.strip()
            if p.startswith(prefix):
                d[p[len(prefix):]] = h
    return d


def compare(name, outdir, exp, extra=None):
    got = {f: sha(os.path.join(outdir, f)) for f in os.listdir(outdir)}
    if extra:
        got.update(extra)
    same = sum(1 for f, h in exp.items() if got.get(f) == h)
    missing = [f for f in exp if f not in got]; diff = [f for f in exp if f in got and got[f] != exp[f]]
    print(f"[repro] {name}: {same}/{len(exp)} bitgleich" + (f", abweichend {diff}" if diff else "") + (f", fehlend {missing}" if missing else ""))
    return 0 if same == len(exp) else 1


def run(cmd, cwd, e, capture=False):
    t = time.time()
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True)
    if r.returncode:
        print(r.stdout.decode()[-2000:], r.stderr.decode()[-4000:]); raise SystemExit(f"FEHLER: {' '.join(cmd)}")
    return r.stdout, time.time() - t


def repro(fast=False):
    guard(); stage(); e = env(); fails = 0
    # 1) Delayed Trend Messung
    for c in ("BTC", "XRP", "DOT"):
        run([PY, "measure_dt_portable.py", c], os.path.join(ROOT, "dt"), e)
    fails += compare("DT-Messung (dt_expected_shas.txt)", os.path.join(ROOT, "dt", "out"),
                     expected("01_forschung/11_delayed_trend/dt_expected_shas.txt", "01_forschung/11_delayed_trend/out/"))
    # 2) XRP v1.0 Outcome-Lauf
    run([PY, "eval_cross_portable.py", "XRP"], os.path.join(ROOT, "rtc"), e)
    fails += compare("XRP v1.0 (xrp_run_2026-09-18_expected_shas.txt)", os.path.join(ROOT, "rtc", "eval_XRP"),
                     expected("00_doku/xrp_run_2026-09-18_expected_shas.txt", "01_forschung/04_xrp_specialist/eval/"))
    # 3) BTC YAMATO Stufe B (inkl. stdout-Log)
    out, _ = run([PY, "eval_btc_b_portable.py", "BTC"], os.path.join(ROOT, "rtc"), e)
    fails += compare("BTC YAMATO Stufe B (yb_expected_shas.txt)", os.path.join(ROOT, "rtc", "eval_BTC_B"),
                     expected("01_forschung/06_btc_specialist/stufeB/yb_expected_shas.txt", "01_forschung/06_btc_specialist/stufeB/eval/"),
                     extra={"eval_BTC_B.log": hashlib.sha256(out).hexdigest()})
    # 4) Stufe 2 Volllauf
    if fast:
        print("[repro] Stufe 2: uebersprungen (--fast)")
    else:
        _, dt = run([PY, "stage2.py", "--tag", "repro"], os.path.join(ROOT, "s2"), e)
        fails += compare_stage2(os.path.join(ROOT, "s2", "out_repro"), dt)
    return fails


def _flat(d, p=""):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from _flat(v, f"{p}/{k}")
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from _flat(v, f"{p}[{i}]")
    else:
        yield p, d


def compare_stage2(out, dt):
    ref = os.path.join(REPO, "01_forschung", "02_strategien")
    a = json.load(open(os.path.join(ref, "stage2_results.json"))); b = json.load(open(os.path.join(out, "stage2_results.json")))
    fa, fb = dict(_flat(a["results"])), dict(_flat(b["results"]))
    nd = sum(1 for k, v in fa.items() if not (v == fb.get(k) or (isinstance(v, float) and isinstance(fb.get(k), float) and math.isnan(v) and math.isnan(fb[k]))))
    vd = sum(1 for k in a["results"] if a["results"][k]["verdict"] != b["results"][k]["verdict"])
    tr = sorted(os.listdir(os.path.join(ref, "stage2_trades")))
    td = [f for f in tr if sha(os.path.join(ref, "stage2_trades", f)) != sha(os.path.join(out, "stage2_trades", f))]
    cfg = sha(os.path.join(ref, "stage2_config_log.csv")) == sha(os.path.join(out, "stage2_config_log.csv"))
    pre = a["prereg_sha256"] == b["prereg_sha256"]
    ok = nd == 0 and vd == 0 and not td and cfg and pre and len(fa) == len(fb)
    print(f"[repro] Stufe 2 ({dt:.0f} s): Urteile {len(a['results']) - vd}/{len(a['results'])} gleich, Felder {len(fa) - nd}/{len(fa)} gleich, "
          f"Trade-Dateien {len(tr) - len(td)}/{len(tr)} bitgleich, Config-Log {'bitgleich' if cfg else 'ABWEICHEND'}, Prereg-SHA {'gleich' if pre else 'ABWEICHEND'}")
    return 0 if ok else 1


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"; fast = "--fast" in sys.argv
    steps = {"verify-frozen": [verify_frozen], "portable": [portable], "tests": [tests], "repro": [lambda: repro(fast)],
             "all": [verify_frozen, portable, tests, lambda: repro(fast)]}[cmd]
    fails = sum(s() for s in steps)
    print(f"== CI {cmd}{' --fast' if fast else ''}: {'OK' if fails == 0 else f'FEHLER ({fails})'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
