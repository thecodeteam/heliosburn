#!/bin/bash


if [ "$EUID" != "0" ]
then
    echo "You must be the root user to run this installer."
    exit 1
fi

echo ">> Creating Django .env file"
cp heliosburn/django/hbproject/example.env heliosburn/django/hbproject/.env
SECRET_KEY=$(openssl rand -hex 16)
sed -i "s/DJANGO_SECRET_KEY.*/DJANGO_SECRET_KEY='$SECRET_KEY'/" heliosburn/django/hbproject/.env

echo ">> Setting up database - executing: 'python heliosburn/django/hbproject/create_db_model.py'"
python heliosburn/django/hbproject/create_db_model.py

echo ">> Collecting static Django assets"
cd heliosburn/django/hbproject
python manage.py collectstatic --noinput

echo ">> Done!"
exit 0
