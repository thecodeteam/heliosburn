#!/bin/sh
echo ">>>>> Installing packages via autoparts"
parts install mongodb
parts install redis

echo ">>>>> Starting installed daemons"
parts start mongodb
parts start redis

echo ">>>>> Creating virtualenv (~/hb_virtualenv)"
mkdir ~/hb_virtualenv
virtualenv -p /usr/bin/python2.7 ~/hb_virtualenv

echo ">>>>> Entering virtualenv"
. ~/hb_virtualenv/bin/activate

echo ">>>>> Installing requirements.txt via pip"
pip install -r requirements.txt

echo ">>>>> Creating .env file"
cp heliosburn/django/hbproject/example.env heliosburn/django/hbproject/.env
SECRET_KEY=$(openssl rand -hex 16)
sed -i "s/DJANGO_SECRET_KEY.*/DJANGO_SECRET_KEY='$SECRET_KEY'/" heliosburn/django/hbproject/.env

echo ">>>>> Creating initial MongoDB model"
python heliosburn/django/hbproject/create_db_model.py

echo ""
echo "-- A Python virtualenv named 'hb_virtualenv' has been created in the home directory. To use it, run 'source ~/hb_virtualenv/bin/activate'."
echo "-- To leave the virtualenv, run 'deactivate'."
echo ""
echo "-- MongoDB and Redis have been started. In the future, you may start them with 'parts start mongodb' and 'parts start redis'".
