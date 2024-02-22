create-env:
	poetry config virtualenvs.in-project true && \
	poetry install
run-tests:
	docker-compose --env-file tests/.env-tests -f docker-compose-test.yml up -d --build && \
	docker-compose --env-file tests/.env-tests -f docker-compose-test.yml exec api pytest -vv&& \
	docker-compose --env-file tests/.env-tests -f docker-compose-test.yml down -v

full-setup:
	make create-env
	poetry run pre-commit install
	poetry run pre-commit run --all-files
	make run-tests
