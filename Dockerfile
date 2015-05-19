FROM ubuntu:latest

ADD requirements.txt /tmp/requirements.txt
ADD heliosburn /opt/HeliosBurn/heliosburn
ADD heliosburn/django/hbproject/example.env /opt/HeliosBurn/heliosburn/django/hbproject/.env
ADD install/docker/modules.yaml /opt/HeliosBurn/heliosburn/proxy/modules.yaml
ADD install/docker/config.yaml /opt/HeliosBurn/heliosburn/proxy/config.yaml

RUN apt-get -y update
RUN apt-get -y install python-software-properties
RUN apt-get -y install git
RUN apt-get -y install curl
RUN apt-get -y install ipython-notebook
RUN apt-get -y install npm
RUN apt-get -y install supervisor
RUN apt-get -y install python
RUN apt-get -y install python-pip
RUN apt-get -y install default-jre
RUN apt-get -y install openssl
RUN apt-get -y install build-essential python-dev
# SECRET_KEY=$(openssl rand -hex 16)
RUN sed -i "s/DJANGO_SECRET_KEY.*/DJANGO_SECRET_KEY="'$(openssl rand -hex 16)'"/" heliosburn/django/hbproject/.env
RUN pip install -r /tmp/requirements.txt
ADD install/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/
ADD install/docker/settings.yaml /opt/HeliosBurn/heliosburn/django/hbproject/hbproject/settings.yaml
RUN python /opt/HeliosBurn/heliosburn/django/hbproject/create_db_model.py
EXPOSE 80
CMD ["/usr/bin/supervisord", "-n"]
