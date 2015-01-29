#!/bin/sh
# init script for Django components of HeliosBurn

workdir=/opt/HeliosBurn/heliosburn/django/hbproject
 
start() {
    cd $workdir
    /usr/bin/python cherrypy_launcher.py &
}
 
stop() {
    pid=`ps -ef | grep '[p]ython cherrypy_launcher.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "Server killed."
}
 
case "$1" in
  start)
    start
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: /etc/init.d/hbdjango.sh {start|stop|restart}"
    exit 1
esac
exit 0
