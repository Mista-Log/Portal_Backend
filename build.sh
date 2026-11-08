#!/usr/bin/env bash

set -o errexit

# Install dependencies from uv.lock
uv sync --frozen --no-dev

# Collect static files
uv run python manage.py collectstatic --no-input

# Apply database migrations
uv run python manage.py migrate