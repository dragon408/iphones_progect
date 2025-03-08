FROM python:3.11
WORKDIR /app

COPY ../Telegram%20Desktop/iphones_progect/app /app/
# COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 5050

CMD ["gunicorn","-w","4","-b","0.0.0.0:5050","main:app"]