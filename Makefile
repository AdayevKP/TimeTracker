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
	docker-compose -f docker-compose-test.yml up -d --build && \
	docker-compose -f docker-compose-test.yml exec api pytest && \
	docker-compose -f docker-compose-test.yml down
