"""Gemeinsame Definition: Legacy-Layout (Claude-Sandbox /home/claude/...) und Manifest der portablen Versionen.

LEGACY_DIRS: Unterordner des Arbeitsbereichs AURUM_ROOT -> Quellordner im Repo (wird beim Staging KOPIERT).
LINKS:       zusaetzliche Eintraege im Arbeitsbereich (Kopie oder Symlink auf grosse, nur gelesene Daten).
PORTABLE:    (Quelle eingefroren, Zielpfad im Arbeitsbereich, Regeln). Die Datei liegt im Repo unter portable/<Ziel>.
Regeln: "paths" = /home/claude -> AURUM_ROOT, "sha_self" = sha(__file__) -> sha der eingefrorenen Originaldatei,
        "cost:NAME=abschnitt" = Modul-Konstante NAME aus config/cost_model_v1.json laden.
"""
LEGACY_DIRS = {
    "rtc": "01_forschung/00_gemeinsam/rlib",
    "yamato": "01_forschung/06_btc_specialist/stufeA",
    "micro": "01_forschung/10_rebound_micro/mlib",
    "micro_audit": "01_forschung/10_rebound_micro/audit",
    "dt": "01_forschung/11_delayed_trend/dtlib",
    "s2": "01_forschung/02_strategien",
    "re": "01_forschung/03_woo_mtp_reverse_engineering",
    "mtp": "01_forschung/03_mtp_validation",
    "ethsol_dev": "01_forschung/07_eth_sol_specialist/dev",
}
# (Ziel im Arbeitsbereich, Quelle im Repo, Art) Art: copy | symlink
LINKS = [
    ("rtc/count_XRP", "01_forschung/04_xrp_specialist/count", "copy"),
    ("rtc/count_DOT", "01_forschung/05_dot_specialist/count", "copy"),
    ("rtc/count_BTC_B", "01_forschung/06_btc_specialist/stufeB/count", "copy"),
    ("holdout", "02_daten/holdout", "symlink"),
    ("pylib", "pylib", "symlink"),
]
P = "paths"
PORTABLE = [
    # Treiber und Tests (nur Pfade)
    ("01_forschung/00_gemeinsam/rlib/eval_cross.py", "rtc/eval_cross_portable.py", [P]),
    ("01_forschung/00_gemeinsam/rlib/eval_btc_b.py", "rtc/eval_btc_b_portable.py", [P]),
    ("01_forschung/00_gemeinsam/rlib/count_cross.py", "rtc/count_cross_portable.py", [P]),
    ("01_forschung/00_gemeinsam/rlib/count_btc_b.py", "rtc/count_btc_b_portable.py", [P]),
    ("01_forschung/00_gemeinsam/rlib/regress_btc.py", "rtc/regress_btc_portable.py", [P]),
    ("01_forschung/00_gemeinsam/rlib/tests/test_rlib.py", "rtc/tests/test_rlib_portable.py", [P]),
    ("01_forschung/06_btc_specialist/stufeA/tests/test_ylib.py", "yamato/tests/test_ylib_portable.py", [P]),
    ("01_forschung/06_btc_specialist/stufeA/count_stufeA.py", "yamato/count_stufeA_portable.py", [P]),
    ("01_forschung/06_btc_specialist/stufeA/eval_stufeA.py", "yamato/eval_stufeA_portable.py", [P]),
    ("01_forschung/06_btc_specialist/stufeA/lookahead_test.py", "yamato/lookahead_test_portable.py", [P]),
    ("01_forschung/10_rebound_micro/mlib/tests/test_mlib.py", "micro/tests/test_mlib_portable.py", [P]),
    ("01_forschung/10_rebound_micro/mlib/tests/test_simulate.py", "micro/tests/test_simulate_portable.py", [P]),
    ("01_forschung/10_rebound_micro/mlib/count_micro.py", "micro/count_micro_portable.py", [P]),
    ("01_forschung/10_rebound_micro/mlib/simulate_micro.py", "micro/simulate_micro_portable.py", [P, "sha_self"]),
    ("01_forschung/10_rebound_micro/mlib/eval_micro.py", "micro/eval_micro_portable.py", [P, "sha_self"]),
    ("01_forschung/10_rebound_micro/mlib/report_coin.py", "micro/report_coin_portable.py", [P]),
    ("01_forschung/10_rebound_micro/audit/cost_audit.py", "micro_audit/cost_audit_portable.py", [P]),
    ("01_forschung/11_delayed_trend/dtlib/measure_dt.py", "dt/measure_dt_portable.py", [P, "sha_self"]),
    ("01_forschung/11_delayed_trend/dtlib/tests/test_dtlib.py", "dt/tests/test_dtlib_portable.py", [P]),
    ("01_forschung/07_eth_sol_specialist/dev/dev_dbctx.py", "ethsol_dev/dev_dbctx_portable.py", [P]),
    ("01_forschung/07_eth_sol_specialist/dev/dev_rebound.py", "ethsol_dev/dev_rebound_portable.py", [P]),
    # Libraries mit zentralem Kostenmodell (ersetzen im Arbeitsbereich die eingefrorene Kopie gleichen Namens)
    ("01_forschung/06_btc_specialist/stufeA/ylib.py", "yamato/ylib.py", ["cost:COST=spot_r"]),
    ("01_forschung/10_rebound_micro/mlib/mlib.py", "micro/mlib.py", [P, "cost:COST=spot_r"]),
    ("01_forschung/02_strategien/s2lib.py", "s2/s2lib.py", ["cost:COST=stage2_perp", "cost:SPOT_REF=stage2_spot_ref"]),
    ("01_forschung/02_strategien/spot_ref.py", "s2/spot_ref_portable.py", ["cost:SPOT=stage2_spot_ref"]),
    ("01_forschung/03_mtp_validation/mtp_val.py", "mtp/mtp_val_portable.py", [P, "cost:COST=spot_r"]),
]
