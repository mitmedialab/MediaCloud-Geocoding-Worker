source venv/bin/activate
nohup celery worker -A geoworker -l info > celery.log &
