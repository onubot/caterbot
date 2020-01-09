git log -1 > commit.log
/home/ubuntu/caterbot/venv/bin/gunicorn app:app -b 0.0.0.0:5000 -D