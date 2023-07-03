FROM python:3.9-slim-buster

WORKDIR /service

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

#CMD ["python3", "auth_service/manage.py", "runserver", "0.0.0.0:8000"]
