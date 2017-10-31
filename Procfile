web: newrelic-admin run-program gunicorn --pythonpath="$PWD/vocatebya" wsgi:application
worker: python vocatebya/manage.py rqworker default