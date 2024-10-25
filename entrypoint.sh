#!/bin/sh

# Source the .env file to load environment variables
if [[ -f .env ]]; then
    source .env
fi

# Wait for database to start listening at port 5432
while ! nc -z $POSTGRES_HOSTNAME $POSTGRES_PORT; do
    echo "Database is not running yet. Will wait for 1 second."
    sleep 1
done

echo "Migrating database..."
python manage.py migrate

# Collect static
python manage.py collectstatic --noinput

echo "Start running the application..."
gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:$APP_PORT invoicer.wsgi:application