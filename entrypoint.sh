#!/bin/bash

if [ ! -f "migrations/env.py" ]; then
  echo "Initializing database migrations..."
  flask db init
fi

echo "Running database migrations..."
flask db migrate
flask db upgrade

echo "Starting application..."
uwsgi app.ini
