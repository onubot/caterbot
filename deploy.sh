git log -1 > commit.log
killall gunicorn
/home/ubuntu/caterbot/venv/bin/gunicorn /home/ubuntu/caterbot/app:app -b 0.0.0.0:5000 -D