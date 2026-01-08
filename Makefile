PIPENV = pipenv
PYTHON = $(PIPENV) run python

install:
	$(PIPENV) install

install-dev:
	$(PIPENV) install --dev

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8085

test:
	PYTHONPATH=. pytest -vv

coverage:
	PYTHONPATH=. pytest --cov=app --cov-report=term-missing

coverage-xml:
	PYTHONPATH=. pytest --cov=app --cov-report=xml --cov-report=term-missing --cov-fail-under=80

sonar: coverage
	pysonar --coverage-report coverage.xml

format:
	black app tests --line-length 120

lint:
	flake8 app tests --max-line-length=120

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache