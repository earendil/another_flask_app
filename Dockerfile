FROM python:3.8.3-alpine

COPY ./flask_app /flask_app/

WORKDIR /flask_app

COPY ./requirements.txt /flask_app/requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn" ]

CMD ["--workers", "8", "--bind", "0.0.0.0:5000",  "wsgi:app"]

ENV PYTHONUNBUFFERED=1
