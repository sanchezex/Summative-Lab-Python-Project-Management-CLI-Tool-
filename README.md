# Project Management CLI

This is a small Python CLI for managing users, projects, and tasks.

Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the CLI (examples):

```bash
python main.py add-user --name "Alex" --email alex@example.com
python main.py add-project --user "Alex" --title "CLI Tool" --description "Build CLI"
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex"
python main.py list-users
python main.py list-projects
python main.py list-tasks
python main.py complete-task --task-id 1
```

Data persistence

Data is stored in `data/data.json` as JSON. The `utils/storage.py` module handles reading and writing.

Testing

Run tests with `pytest`:

```bash
pytest -q
```

Notes

- Models are in the `models/` package. CLI is in `main.py` using `argparse`.
- Uses `rich` for table output.
- Known limitations: simple JSON storage, no concurrency handling, minimal validation.
