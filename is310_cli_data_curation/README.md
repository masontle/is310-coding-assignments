# IS310 Command Line Data Curation

A Python CLI for entering local cultural events (name, type, venue, date, and admission). Entries are shown in a Rich table, confirmed, and saved to `cultural_events.json` beside the script. Existing entries are preserved between runs.

The bundled sample records are fictional. Delete `cultural_events.json` to start with an empty collection.

## Setup

Use Python 3.10 or newer. From this folder, create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux, activate with `source .venv/bin/activate`. If PowerShell blocks activation, run with the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe cli_data_entry.py
```

## Run

```powershell
python cli_data_entry.py
```

Enter each field; use `unknown` when needed. Blank values are prompted again, and dates and admission are stored as text. Confirm each entry with `y` or `n`, then choose whether to add another. Saved records are written immediately. If the existing JSON file is invalid, the program reports the problem and leaves it untouched.
