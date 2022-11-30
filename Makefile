SHELL := /usr/bin/env bash

.PHONY: unit
unit:
	poetry run pytest

.PHONY: mypy
mypy:
	poetry run mypy isis

.PHONY: lint
lint:
	poetry run pylint isis

.PHONY: test
test: mypy lint unit