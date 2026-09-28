PYTHON ?= python

.PHONY: install test lint run docker-up docker-down

install:
	$(PYTHON) -m pip install -r app/requirements.txt pytest ruff

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check app tests

run:
	cd app && $(PYTHON) -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v
