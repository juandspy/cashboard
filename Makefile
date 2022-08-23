SHELL := /bin/bash

.PHONY: default init run test help

MAIN_PATH=./ui/main.py
VENV_PATH=./venv
THIS_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))

default: run

init: ## Initialize the environment
	export PYTHONPATH=${THIS_DIR}

run: init ## Run the UI
	${VENV_PATH}/bin/python3 -m streamlit run ${MAIN_PATH} --server.headless true

test: init ## Run unit tests and integration tests
	${VENV_PATH}/bin/python3 -m pytest

style:
	pre-commit run --all-files

help: ## Show this help screen
	@echo 'Usage: make <OPTIONS> ... <TARGETS>'
	@echo ''
	@echo 'Available targets are:'
	@echo ''
	@grep -E '^[ a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ''
