.PHONY: help pull-deploy push-deploy makemigrations migrate runserver createsuperuser collectstatic test install-nginx uninstall-nginx install-gunicorn uninstall-gunicorn lint format check-lint check-types check-all pre-commit-install pre-commit-run

# Makefile

help:			## Show this help.
	@echo "Available commands:"
	@echo "For more information, see the README.md file."
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Define a guard function to check for DEBUG mode
debug_wrap:
	@if [ "$(DEBUG)" != "True" ]; then \
		echo "Error: This operation is only allowed in DEBUG mode. Set DEBUG=1 to proceed."; \
		exit 1; \
	fi

makemigrations: ## Make migrations
	python manage.py makemigrations

migrate: makemigrations ## Apply migrations
	python manage.py migrate

runserver: migrate  ## Run the Django development server
	python manage.py runserver 0.0.0.0:8000

superuser: ## Create a superuser
	@python manage.py createsuperuser --no-input

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

test: ## Run tests
	pytest . -n auto

# === Code Quality & Linting ===

format: ## Auto-format code with Black and Ruff
	@echo "Running Black formatter..."
	black .
	@echo "Running Ruff formatter..."
	ruff format .
	@echo "Running Ruff auto-fixes..."
	ruff check --fix .

check-lint: ## Check code with Ruff linter (no auto-fix)
	@echo "Running Ruff linter..."
	ruff check .

lint: ## Run Ruff linter with auto-fix
	@echo "Running Ruff linter with auto-fix..."
	ruff check --fix .

check-types: ## Run mypy type checker
	@echo "Running mypy type checker..."
	mypy .

check-all: check-lint check-types ## Run all code quality checks
	@echo "All code quality checks completed!"

pre-commit-install: ## Install pre-commit hooks
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "Pre-commit hooks installed. They will run automatically on git commit."

pre-commit-run: ## Run pre-commit on all files
	@echo "Running pre-commit on all files..."
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks to latest versions
	@echo "Updating pre-commit hooks..."
	pre-commit autoupdate

ci-lint: ## Run CI-style linting (used in CI/CD)
	@echo "Running CI linting checks..."
	ruff check .
	black --check .
	mypy .
	@echo "CI linting passed!"

flush: debug_wrap ## Flush the database (delete all data!)
	@if [ -z "$(DEBUG)" ]; then python manage.py flush; else python manage.py flush --noinput; fi




clean:		## Remove pycache, tmp files and test db, mail, etc
	find . -name "*.pyc" -delete
	-find $(CURDIR) -type d -path "*__pycache__*" -not -path "*/.venv/*" -exec rm -rf {} \; #> /dev/null 2>&1
	./manage.py drop_test_database --noinput

schema:                 ## Use DRF Spectacular to generate schema for codegen to a python client
	python manage.py spectacular --api-version v1 --file schema.yaml


journal: ## View all relevant logs
	journalctl -f -n 50 -u gunicorn -u rm-queue -u rm-server -u nginx


rm-migrations: debug_wrap ## Delete all migrations
	@read -p "Delete ALL migrations? [y/N] " confirm; \
	if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
		exit 1; \
	fi
	rm **/migrations/0*.py
	rm */*/migrations/0*.py
	echo Deleted all migrations. Run 'make migrate' to recreate them.
