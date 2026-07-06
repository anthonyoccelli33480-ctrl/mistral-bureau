.PHONY: install backend frontend

install:
	cd backend && uv venv --python 3.12 .venv && uv pip install -r requirements.txt --python .venv/bin/python
	cd frontend && npm install

backend:
	cd backend && .venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8789

frontend:
	cd frontend && npm run dev