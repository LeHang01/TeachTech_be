1/ RUN SERVER : python manage.py runserver

2/ RUN CELERY : celery -A be_teachtech worker --loglevel=info --concurrency=1 -P solo