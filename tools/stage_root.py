#!/usr/bin/env python3
"""Baut den Arbeitsbereich AURUM_ROOT (Default build/root) im Layout der Claude-Sandbox.

Eingefrorene Dateien werden KOPIERT (Skripte koennen so nie in eingefrorene Repo-Dateien schreiben),
grosse, nur gelesene Daten (02_daten/holdout, data/raw) werden verlinkt. Danach werden die portablen
Versionen aus portable/ darueber kopiert. Der Arbeitsbereich wird bei jedem Aufruf neu erstellt.
"""
import os, shutil, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
from aurum_layout import LEGACY_DIRS, LINKS, PORTABLE

IGN = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache")


def main():
    root = os.path.abspath(os.environ.get("AURUM_ROOT") or os.path.join(REPO, "build", "root"))
    assert os.path.realpath(root).startswith(os.path.realpath(os.path.join(REPO, "build"))) or os.environ.get("AURUM_ROOT_ALLOW_ANY") == "1", \
        f"AURUM_ROOT {root} liegt ausserhalb von build/ (setze AURUM_ROOT_ALLOW_ANY=1, wenn gewollt)"
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    for dst, src in LEGACY_DIRS.items():
        shutil.copytree(os.path.join(REPO, src), os.path.join(root, dst), ignore=IGN, symlinks=False)
    for dst, src, kind in LINKS:
        d, s = os.path.join(root, dst), os.path.join(REPO, src)
        if kind == "copy":
            shutil.copytree(s, d, ignore=IGN)
        else:
            os.symlink(s, d)
    # Stufe-2-Rohdaten: s2/raw = Links auf data/raw/* plus Ergaenzung DTB3
    raw = os.path.join(REPO, "data", "raw")
    if os.path.isdir(raw):
        s2raw = os.path.join(root, "s2", "raw"); os.makedirs(s2raw)
        for e in sorted(os.listdir(raw)):
            os.symlink(os.path.join(raw, e), os.path.join(s2raw, e))
        sup = os.path.join(REPO, "data", "supplement", "DTB3_3m_tbill.csv")
        if os.path.exists(sup) and not os.path.exists(os.path.join(s2raw, "DTB3_3m_tbill.csv")):
            shutil.copy2(sup, os.path.join(s2raw, "DTB3_3m_tbill.csv"))
    else:
        print("WARNUNG: data/raw fehlt (make data), Stufe-2-Reproduktion nicht moeglich")
    for _, stage, _ in PORTABLE:
        d = os.path.join(root, stage); os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(REPO, "portable", stage), d)
    print(f"Arbeitsbereich bereit: {root}")


if __name__ == "__main__":
    main()
