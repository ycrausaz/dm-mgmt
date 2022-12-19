release: python manage.py migrate
web: gunicorn --pythonpath dm_mgmt mgmt.wsgi --log-file -
