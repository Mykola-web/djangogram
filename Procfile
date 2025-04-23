release: cd insta && python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate
web: cd insta && gunicorn insta.wsgi:application --bind 0.0.0.0:$PORT
