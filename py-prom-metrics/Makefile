.PHONY: venv run-local run-docker clean

venv:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r app/requirements.txt

run-local: venv
	. .venv/bin/activate && APP_NAME=py-prom-demo PORT=8000 python app/app.py

run-docker:
	docker compose up --build

clean:
	rm -rf .venv __pycache__ */__pycache__
