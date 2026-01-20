# Heroku/Railway Procfile
web: gunicorn tracking_site.wsgi:application --bind 0.0.0.0:$PORT --workers 4
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
