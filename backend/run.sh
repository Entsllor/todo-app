sleep 2 # waiting for DB
(cd src/ && flask db upgrade head; cd ..)
gunicorn "src.app:app" -b 0.0.0.0:5000
