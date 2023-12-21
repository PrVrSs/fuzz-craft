SHELL := /usr/bin/env bash

.PHONY: unit
unit:
	poetry run pytest

.PHONY: mypy
mypy:
	poetry run mypy fuzz_craft

.PHONY: lint
lint:
	poetry run pylint fuzz_craft

.PHONY: test
test: mypy lint unit