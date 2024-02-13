#!/bin/bash

alembic upgrade head
uvicorn time_tracker.app:app --host 0.0.0.0 --port 80 --reload
