release: cd insta && python manage.py migrate && python manage.py collectstatic --noinput
web: cd insta && gunicorn insta.wsgi:application --bind 0.0.0.0:$PORT

