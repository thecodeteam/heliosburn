#!/bin/bash

echo ">> Creating Django .env file"
cp heliosburn/django/hbproject/example.env heliosburn/django/hbproject/.env
SECRET_KEY=$(openssl rand -hex 16)
sed -i "s/DJANGO_SECRET_KEY.*/DJANGO_SECRET_KEY='$SECRET_KEY'/" heliosburn/django/hbproject/.env

echo ">> Setting up database - executing: 'python heliosburn/django/hbproject/create_db_model.py'"
python heliosburn/django/hbproject/create_db_model.py

echo ">> Installing Bower components"
cd heliosburn/django/hbproject
python manage.py bower install

echo ">> Collecting static Django assets"
python manage.py collectstatic --noinput

echo ">> Done!"
exit 0
