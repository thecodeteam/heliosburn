#!/bin/bash
PWD=$(pwd)


if [ "$EUID" != "0" ]
then
    echo "You must be the root user to run this installer."
    exit 1
fi

echo ">> Copying installation files to /opt/HeliosBurn"
cp -rf /home/vagrant/HeliosBurn /opt/
cd /opt/HeliosBurn

echo ">> Creating Django .env file"
cp heliosburn/django/hbproject/example.env heliosburn/django/hbproject/.env
SECRET_KEY=$(openssl rand -hex 16)
sed -i "s/DJANGO_SECRET_KEY.*/DJANGO_SECRET_KEY='$SECRET_KEY'/" heliosburn/django/hbproject/.env

echo ">> Installing supervisord profiles under /etc/supervisor/conf.d/"
install -b install/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/
echo ">> Setting up database - executing: 'python heliosburn/django/hbproject/create_db_model.py'"
python heliosburn/django/hbproject/create_db_model.py
echo ">> Collecting static Django assets"
cd heliosburn/django/hbproject
python manage.py collectstatic --noinput
echo ">> Restarting supervisord"
/etc/init.d/supervisor restart
echo ">> Installation complete!"
echo ">> On your host OS, browse to http://127.0.0.1:8100 and login as 'admin' / 'admin'"
exit 0
cd $PWD

