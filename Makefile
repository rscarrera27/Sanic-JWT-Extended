.PHONY: env check format clean

POETRY := $(shell poetry --version 2> /dev/null)

env:
ifndef POETRY
	@echo Poetry not found. install poetry
	curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
	@echo Please re-execute this command to install dependencies
endif
	@echo Poetry found. install dependencies.
	poetry install

check:
	isort --recursive --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=88 --check-only sanic_jwt_extended tests
	black -S --check sanic_jwt_extended tests
	pylint sanic_jwt_extended

format:
	isort -rc -y --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=88 sanic_jwt_extended tests
	black -S sanic_jwt_extended tests

clean:
	rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./out ./*/out ./.mypy_cache ./*/.mypy_cache

