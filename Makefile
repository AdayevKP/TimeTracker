build-docker:
	docker build -t time-tracker .
start-docker:
	docker run -d -p 8080:80 time-tracker
create-env:
	poetry config virtualenvs.in-project true && \
	poetry install
update-env:
	poetry update
run-tests:
	docker-compose --env-file tests/.env-tests -f docker-compose-test.yml up -d --build && \
	docker-compose --env-file tests/.env-tests -f docker-compose-test.yml exec api pytest -vv&& \
	docker-compose -f docker-compose-test.yml down -v
