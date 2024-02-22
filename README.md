# TimeTracker Backend

Simple service for tracking your time. It is my educational project.

Web UI for this project: https://github.com/AdayevKP/TimeTrackerUI

# Getting started for demo/frontend dev
1. create `.env` file in project root directory (you can just copy content of tests/.env-tests)
2. run `docker-compose up` from project root
3. checkout docs at `http://0.0.0.0:80/docs`

# Getting started for backend development
  Make sure that you have `make` installed in your system (for mac `brew install make`)
  Install python3.12 and pip install poetry
  
0. create `.env` file in project root directory (you can just copy content of tests/.env-tests)
 
  Run `make full-setup` for full setup (if you trust me) or execute step by step:
1. install venv `make create-env`
3. install pre-commit hooks `poetry run pre-commit install`
4. run all mypy and style checks `poetry run pre-commit run --all-files`
5. run tests `make run-tests`

If nothing failed you're good to go ;)
