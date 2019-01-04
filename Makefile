PROJECT_NAME=dicom_api

# Common

lint:
	black --check .
	flake8 dicom_api tests setup.py

format:
	isort -rc dicom_api tests setup.py
	black .

test_unit:
	pytest -vv tests/unit

test_integration:
	pytest -vv tests/integration



all: run

run:
	@docker-compose up dicom_api dcmrecv

stop:
	@docker-compose stop

clean:
	@docker-compose down

bash:
	@docker exec -it dicom_api bash

# Docs

doc:
	cd docs && make html

# Linters & tests

mypy:
	@docker-compose run --rm $(PROJECT_NAME)_app mypy $(PROJECT_NAME)

lint:
	@docker-compose run --rm $(PROJECT_NAME)_app flake8 $(PROJECT_NAME)

_test:
	# todo: remove no:warnings
	@py.test -p no:warnings --cov

test: lint
	@docker-compose up test
	@docker-compose stop test

run_production:
	@docker-compose -f docker-compose.yml -f docker-compose.production.yml up

adev:
	adev runserver ./dicom_api/__main__.py -p 8080
