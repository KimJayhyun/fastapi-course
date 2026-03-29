source .venv/bin/activate

PYTHONPATH=./TodoApp uvicorn TodoApp.main:app --reload