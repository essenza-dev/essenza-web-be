#!/bin/bash
set -e

echo "Starting Django application startup script..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
until python manage.py check --database default; do
  echo "Database is not ready yet, waiting 5 seconds..."
  sleep 5
done

echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Check if migrations were successful
if [ $? -eq 0 ]; then
    echo "Migrations completed successfully!"
else
    echo "Migration failed!" >&2
    exit 1
fi

# Collect static files (in case of updates)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn server..."
exec "$@"