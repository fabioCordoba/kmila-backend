FROM python:3.13-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
# Allows docker to cache installed dependencies between builds
COPY requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

# Installing dependencies
RUN pip install gunicorn

RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . /code

EXPOSE 8000

# RUN python manage.py migrate

CMD ["gunicorn", "--config", "gunicorn_config.py", "kmila.wsgi:application"]