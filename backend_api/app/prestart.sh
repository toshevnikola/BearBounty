#! /usr/bin/env

# Let the DB start
python /app/backend_pre_start.py

# Run migrations
alembic upgrade head

