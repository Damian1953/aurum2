# Aurum II – lokale Werkzeuge. Python aus .venv (siehe requirements.lock).
PY ?= .venv/bin/python
export PYTHONDONTWRITEBYTECODE=1

.PHONY: help venv data portable portable-check stage test repro repro-fast verify-frozen ci ci-fast hooks collect

help:
	@echo "make venv          .venv aus requirements.lock erzeugen"
	@echo "make data          Rohdaten nach data/raw kopieren + Symlink 02_daten/raw (Quelle: AURUM_DATA_SRC=...)"
	@echo "make portable      portable/ aus den Originalen neu erzeugen"
	@echo "make stage         Arbeitsbereich build/root aufbauen"
	@echo "make test          34 eingefrorene Tests + Repo-Tests"
	@echo "make repro         4 Reproduktionen (DT, XRP, BTC Stufe B, Stufe 2 ~5 min)"
	@echo "make repro-fast    Reproduktionen ohne Stufe 2"
	@echo "make verify-frozen Originale + Expected-SHA-Listen + Holdout-Manifest pruefen"
	@echo "make ci            alles (lokale CI)"
	@echo "make ci-fast       alles ausser Stufe 2 (pre-commit)"
	@echo "make hooks         pre-commit-Hook aktivieren"
	@echo "make collect       taeglichen Datensammler einmal ausfuehren"

venv:
	python3 -m venv .venv && .venv/bin/pip install -q -r requirements.lock

data:
	tools/link_data.sh

portable:
	$(PY) tools/make_portable.py

portable-check:
	$(PY) tools/ci.py portable

stage:
	$(PY) tools/stage_root.py

test:
	$(PY) tools/ci.py tests

repro:
	$(PY) tools/ci.py repro

repro-fast:
	$(PY) tools/ci.py repro --fast

verify-frozen:
	$(PY) tools/ci.py verify-frozen

ci:
	$(PY) tools/ci.py all

ci-fast:
	$(PY) tools/ci.py all --fast

hooks:
	git config core.hooksPath .githooks && echo "pre-commit-Hook aktiv (make ci-fast)"

collect:
	collector/run_collector.sh
