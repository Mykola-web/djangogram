release: cd insta && python manage.py collectstatic --noinput && makemigrations && migrate
web: cd insta && gunicorn insta.wsgi:application --bind 0.0.0.0:$PORT

