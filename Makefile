.PHONY: minimum-requirements
minimum-requirements:
	@pip install -r requirements.txt

.PHONY: dev-requirements
dev-requirements:
	@pip install -r requirements.dev.txt

.PHONY: requirements
## install all requirements
requirements: dev-requirements minimum-requirements

.PHONY: tests
tests:
	@pytest -W ignore::DeprecationWarning --cov=pyspark_pipeline --cov-report term --cov-report html:htmlcov  --cov-fail-under=100 --ignore=tests/e2e tests

.PHONY: unit-tests
unit-tests:
	@echo ""
	@echo "Unit Tests"
	@echo "=========="
	@echo ""
	@pytest -W ignore::DeprecationWarning --cov=pyspark_pipeline tests/unit

.PHONY: integration-tests
integration-tests:
	@echo ""
	@echo "Integration Tests"
	@echo "================="
	@echo ""
	@pytest -W ignore::DeprecationWarning --cov=pyspark_pipeline tests/integration

.PHONY: e2e-tests
## run e2e tests with infrastructure on docker compose
e2e-tests:
	@echo ""
	@echo "E2E Tests"
	@echo "================="
	@echo ""
	@docker compose -f tests/e2e/docker-compose.yaml up --build e2e

.PHONY: app
## create db and run am interactive shell with all dependencies installed.
app:
	@docker build -t app .
	@docker compose -f tests/e2e/docker-compose.yaml run app bash

.PHONY: teardown
## teardown all infra on docker compose
teardown:
	@docker compose -f tests/e2e/docker-compose.yaml down

.PHONY: black
black:
	@black --exclude="build/|buck-out/|dist/|_build/|pip/|\.pip/|\.git/|\.hg/|\.mypy_cache/|\.tox/|\.venv/" .

.PHONY: isort
isort:
	@isort pyspark_pipeline
	@isort tests

.PHONY: apply-style
apply-style:
	@make black
	@make isort

.PHONY: style-check
style-check:
	@echo ""
	@echo "Code Style"
	@echo "=========="
	@echo ""
	@python -m black --check --exclude="build/|buck-out/|dist/|_build/|pip/|\.pip/|\.git/|\.hg/|\.mypy_cache/|\.tox/|\.venv/" . && echo "\n\nSuccess" || echo "\n\nFailure\n\nRun \"make black\" to apply style formatting to your code"
	@echo ""

.PHONY: check-flake8
check-flake8:
	@echo ""
	@echo "Flake 8"
	@echo "======="
	@echo ""
	@python -m flake8 pyspark_pipeline/ && echo "pyspark_pipeline module success"
	@python -m flake8 tests/ && echo "tests module success"
	@echo ""

.PHONY: type-check
## run static type checks
type-check:
	@echo ""
	@echo "mypy"
	@echo "===="
	@echo ""
	@python -m mypy --no-warn-unused-ignores pyspark_pipeline

.PHONY: checks
checks:
	@echo ""
	@echo "Black code style, Flake 8 and Mypy"
	@echo "--------------------"
	@echo ""
	@make style-check
	@make check-flake8
	@make type-check
	@echo ""

.PHONY: clean
clean:
	@find ./ -type d -name 'htmlcov' -exec rm -rf {} +;
	@find ./ -type d -name 'coverage.xml' -exec rm -rf {} +;
	@find ./ -type f -name 'coverage-badge.svg' -exec rm -f {} \;
	@find ./ -type f -name '.coverage' -exec rm -f {} \;
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;

.PHONY: version
version:
	@grep __version__ setup.py | head -1 | cut -d \" -f2 | cut -d \' -f2 > .version

.PHONY: package-name
package-name:
	@grep __package_name__ setup.py | head -1 | cut -d \" -f2 | cut -d \' -f2 > .package_name

.PHONY: repository-url
repository-url:
	@grep __repository_url__ setup.py | head -1 | cut -d \" -f2 | cut -d \' -f2 > .repository_url

.PHONY: package
package:
	@python -m setup sdist bdist_wheel
