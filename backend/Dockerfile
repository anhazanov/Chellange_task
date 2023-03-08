FROM python:3.10

ARG CUID=1000

# disable create cashe's files
ENV PYTHONDONTWRITEBYTECODE 1
# disbale buffering messages
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN groupadd --gid $CUID django && useradd --uid $CUID --gid django --shell /bin/bash -create-home django

WORKDIR /home/django/app

COPY . .

RUN pip install -r requirements.txt

USER django

#CMD ["gunicorn","-b","0.0.0.0:8001","main_app.wsgi:application"]

