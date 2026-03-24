#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

# Ye code automatically aapka Admin user aur Password bana dega
export DJANGO_SUPERUSER_PASSWORD=kartik123
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

# Ye code automatically pehle se items aur sale add kar dega dashboard me
python load_data.py
