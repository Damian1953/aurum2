#!/bin/bash
# Project Aurum II — Kurshistorie nachladen (Doppelklick im Finder)
# Laeuft direkt auf dem Mac. Beim ersten Start fragt macOS allenfalls nach
# Zugriff auf den Ordner Dokumente. Das ist einmalig zu bestaetigen.
cd "$(dirname "$0")" || exit 1
echo "Project Aurum II — Nachladen der Kurshistorie"
echo "Ordner: $(pwd)"
echo
python3 nachladen_historie.py "$@"
echo
echo "Fertig. Fenster kann geschlossen werden."
read -r -p "Enter zum Schliessen..." _
