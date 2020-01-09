killall gunicorn
/home/ubuntu/caterbot/venv/bin/gunicorn -b 0.0.0.0:5000 app:app -D