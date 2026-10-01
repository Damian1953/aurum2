"""Prueft, dass das zentrale Kostenmodell wortgleich mit den eingefrorenen Konstanten ist (Typ und Wert)."""
import ast, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "pylib"))
import aurum_costs as AC


def _lit(node):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict" and not node.args:
        return {kw.arg: _lit(kw.value) for kw in node.keywords}
    if isinstance(node, ast.Dict):
        return {_lit(k): _lit(v) for k, v in zip(node.keys, node.values)}
    return ast.literal_eval(node)


def frozen(rel, name):
    tree = ast.parse(open(os.path.join(REPO, rel), encoding="utf-8").read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return _lit(n.value)
    raise AssertionError(f"{name} nicht gefunden in {rel}")


def same(a, b):
    assert list(a) == list(b)  # gleiche Schluessel in gleicher Reihenfolge
    for k in a:
        if isinstance(a[k], dict):
            same(a[k], b[k])
        else:
            assert type(a[k]) is type(b[k]) and a[k] == b[k], (k, a[k], b[k])


def test_spot_r_matches_all_frozen_copies():
    c = AC.load("spot_r")
    for rel in ("01_forschung/06_btc_specialist/stufeA/ylib.py", "01_forschung/10_rebound_micro/mlib/mlib.py",
                "01_forschung/03_mtp_validation/mtp_val.py"):
        same(frozen(rel, "COST"), c)


def test_stage2_matches_frozen():
    same(frozen("01_forschung/02_strategien/s2lib.py", "COST"), AC.load("stage2_perp"))
    same(frozen("01_forschung/02_strategien/s2lib.py", "SPOT_REF"), AC.load("stage2_spot_ref"))
    same(frozen("01_forschung/02_strategien/spot_ref.py", "SPOT"), AC.load("stage2_spot_ref"))


def test_load_returns_copies():
    a = AC.load("spot_r"); a["K1"]["fee"] = 9.0
    assert AC.load("spot_r")["K1"]["fee"] == 0.0040


def test_dtlib_bp_constants_derive_from_spot_r_k1():
    """dtlib (eingefroren, nicht portabel umgeschrieben) haelt K1 als abgeleitete Basispunkte:
    Stop-Roundtrip = 2*(fee+fric) + slip_in + slip_sl, Ziel-Roundtrip = 2*(fee+fric) + slip_in."""
    k = AC.load("spot_r")["K1"]
    tree = ast.parse(open(os.path.join(REPO, "01_forschung/11_delayed_trend/dtlib/dtlib.py"), encoding="utf-8").read())
    kw = {k_.arg: k_.value.value for n in ast.walk(tree) if isinstance(n, ast.Call)
          for k_ in n.keywords if k_.arg in ("k1_roundtrip_stop_bp", "k1_roundtrip_target_bp")}
    assert round((2 * (k["fee"] + k["fric"]) + k["slip_in"] + k["slip_sl"]) * 1e4, 6) == kw["k1_roundtrip_stop_bp"] == 99.0
    assert round((2 * (k["fee"] + k["fric"]) + k["slip_in"]) * 1e4, 6) == kw["k1_roundtrip_target_bp"] == 89.0
