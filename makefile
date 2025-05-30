SHELL := /bin/bash

# Prepend venv “bin” to PATH so python3, pip, and tools come from .venv
export PATH := .venv/bin:$(PATH)

.PHONY: create-venv activate-venv activate-venv-win install lint lintfix start-backend start-backend-win start-frontend start-frontend-win init

# ──────────── ENVIRONMENT SETUP ────────────

create-venv:
	python3 -m venv .venv

activate-venv:
	. .venv/bin/activate && echo "🐍 venv activated (subshell only)"

activate-venv-win:
	.\.venv\Scripts\Activate.ps1

# ──────────── DEPENDENCIES ────────────

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

# ──────────── LINTING & FORMATTING ────────────

lint:
	python3 -m flake8 src/ tests/ app.py

lintfix:
	python3 -m black .
	python3 -m isort .
	python3 -m autoflake --remove-all-unused-imports --remove-unused-variables \
		--in-place -r .

# ──────────── RUNNING SERVICES ────────────

start-backend:
	. .venv/bin/activate && uvicorn src.vpp.main:app --reload

start-backend-win:
	.\.venv\Scripts\Activate.ps1 ; uvicorn src.vpp.main:app --reload

start-frontend:
	. .venv/bin/activate && streamlit run app.py

start-frontend-win:
	.\.venv\Scripts\Activate.ps1 ; streamlit run app.py

# ──────────── EVERYTHING AT ONCE ────────────

init: create-venv install lint
