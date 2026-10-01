"""Zentrales Kostenmodell (einzige Quelle). Laedt config/cost_model_v1.json.

Pfad ueberschreibbar mit AURUM_COST_MODEL. Rueckgabe sind frische dicts (in Dateireihenfolge),
damit kein Aufrufer die gemeinsame Quelle veraendern kann.
"""
import json, os, copy

_DEFAULT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config", "cost_model_v1.json")


def path():
    return os.environ.get("AURUM_COST_MODEL") or os.path.normpath(_DEFAULT)


def _model():
    with open(path(), encoding="utf-8") as fh:
        return json.load(fh)


def load(section):
    """Werte eines Abschnitts, z.B. load('spot_r') -> {'K0': {...}, 'K1': {...}, 'K2': {...}}."""
    m = _model()
    if section not in m["sections"]:
        raise KeyError(f"Kostenabschnitt {section!r} fehlt in {path()}")
    v = copy.deepcopy(m["sections"][section]["values"])
    _check(v, section)
    return v


def version():
    return _model()["version"]


def _check(v, section):
    def num(x, where):
        if not isinstance(x, float) or not (0.0 <= x < 2.0):
            raise ValueError(f"Kostenwert {where}={x!r} in {section} ungueltig (float 0..2 erwartet)")
    def walk(d, where):
        for k, x in d.items():
            if isinstance(x, dict):
                walk(x, f"{where}{k}.")
            else:
                num(x, f"{where}{k}")
    walk(v, "")
