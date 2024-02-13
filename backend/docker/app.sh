#!/bin/bash

alembic upgrade head
uvicorn app.app:app --host 0.0.0.0 --port 80 --reload
