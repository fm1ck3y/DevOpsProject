FROM python:alpine

EXPOSE 5001

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["python3","run.py"]
