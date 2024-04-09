python -m venv .venv

.venv/bin/pip install .

.venv/bin/pyinstaller GamePile-API/main.py --onefile -y -n GamePile-API
