#!/usr/bin/env python3
"""Erzeugt die portablen Versionen unter portable/ deterministisch aus den eingefrorenen Originalen.

  python tools/make_portable.py          # schreibt portable/
  python tools/make_portable.py --check  # prueft, dass portable/ exakt der Transformation entspricht (CI)

Die Transformation ist rein mechanisch (siehe REPRODUCIBILITY.md). Dadurch bleibt jede portable Datei
nachweisbar «Original modulo Pfad/Kostenquelle», und die in den Laeufen festgehaltene Skript-SHA (Original) bleibt aussagekraeftig.
"""
import ast, hashlib, os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
from aurum_layout import PORTABLE


def transform(src_rel, stage_rel, rules):
    raw = open(os.path.join(REPO, src_rel), encoding="utf-8").read()
    sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    lines = raw.split("\n")
    # 1) Kosten: Modul-Konstante durch zentrale Quelle ersetzen (Zeilenbereich per AST)
    repl = {}
    tree = ast.parse(raw)
    for r in rules:
        if not r.startswith("cost:"):
            continue
        name, section = r[5:].split("=")
        node = next((n for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1
                     and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name), None)
        assert node is not None, (src_rel, name)
        assert node.col_offset == 0 and lines[node.lineno - 1].startswith(name), (src_rel, name)
        tail = lines[node.end_lineno - 1][node.end_col_offset:]
        assert tail.strip() == "" or tail.strip().startswith("#"), (src_rel, name, tail)
        repl[node.lineno] = (node.end_lineno, f'{name} = _ac.load("{section}"){tail}  # zentral: config/cost_model_v1.json [{section}]')
    out, i = [], 1
    while i <= len(lines):
        if i in repl:
            end, txt = repl[i]; out.append(txt); i = end + 1
        else:
            out.append(lines[i - 1]); i += 1
    body = "\n".join(out)
    # 2) Pfade
    if "paths" in rules:
        n0 = body.count("/home/claude")
        body = body.replace('f"/home/claude', '_AR + f"').replace('"/home/claude', '_AR + "')
        assert n0 > 0 and "/home/claude" not in body, (src_rel, "Pfadersetzung unvollstaendig")
    # 3) Skript-SHA auf das eingefrorene Original zeigen lassen
    if "sha_self" in rules:
        assert "sha(__file__)" in body, src_rel
        body = body.replace("sha(__file__)", "sha(_FROZEN_SELF)")
    depth = stage_rel.count("/")
    up = "/".join([".."] * depth)
    frozen_name = os.path.basename(src_rel)
    hdr = [
        f"# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.",
        f"# Quelle (eingefroren): {src_rel}  sha256 {sha}",
        f"# Regeln: {', '.join(rules)}. Arbeitsbereich: AURUM_ROOT (Default: Ordner {up!r} relativ zu dieser Datei).",
        f'import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), "{up}"))',
    ]
    if "sha_self" in rules:
        hdr.append(f'_FROZEN_SELF = _aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), "{frozen_name}")  # eingefrorenes Original im Arbeitsbereich')
    if any(r.startswith("cost:") for r in rules):
        hdr.append('try:\n    import aurum_costs as _ac\nexcept ImportError:\n    import sys as _asys; _asys.path.append(_aos.path.join(_AR, "pylib")); import aurum_costs as _ac')
    return "\n".join(hdr) + "\n" + body


def main():
    check = "--check" in sys.argv
    bad = 0
    for src, stage, rules in PORTABLE:
        new = transform(src, stage, rules)
        dst = os.path.join(REPO, "portable", stage)
        if check:
            cur = open(dst, encoding="utf-8").read() if os.path.exists(dst) else None
            if cur != new:
                print(f"ABWEICHUNG: portable/{stage} entspricht nicht der Transformation von {src}"); bad += 1
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, "w", encoding="utf-8").write(new)
    # keine verwaisten Dateien in portable/
    known = {os.path.join(REPO, "portable", s) for _, s, _ in PORTABLE}
    for root, _, files in os.walk(os.path.join(REPO, "portable")):
        for f in files:
            p = os.path.join(root, f)
            if f.endswith(".py") and p not in known:
                print(f"UNBEKANNT: {os.path.relpath(p, REPO)}"); bad += 1
    print(f"make_portable: {len(PORTABLE)} Dateien, {'Pruefung' if check else 'geschrieben'}, Abweichungen {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
