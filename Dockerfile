FROM ubuntu:latest

ADD requirements.txt /tmp/requirements.txt
ADD heliosburn /opt/heliosburn

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
RUN apt-get -y install build-essential python-dev
RUN pip install -r /tmp/requirements.txt
ADD install/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/
#RUN python /opt/heliosburn/django/hbproject/create_db_model.py
EXPOSE 80
CMD ["/usr/bin/supervisord -n"]
