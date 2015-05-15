FROM ubuntu:latest

RUN apt-get -y update
ADD puppet /tmp/puppet
ADD requirements.txt /tmp/requirements.txt
ADD heliosburn /opt/heliosburn
RUN apt-get -y install puppet
RUN puppet apply --modulepath=/tmp/puppet/modules /tmp/puppet/manifests/default.pp
RUN rm -rf /tmp/puppet
ADD install/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/
RUN python /opt/heliosburn/django/hbproject/create_db_model.py
EXPOSE 22 80
CMD ["/usr/bin/supervisord"]
