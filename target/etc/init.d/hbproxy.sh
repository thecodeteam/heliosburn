#!/bin/sh
# init script for Django components of HeliosBurn

workdir=/opt/HeliosBurn/heliosburn/proxy
 
start() {
    cd $workdir
    /usr/bin/python proxy_core.py &
}
 
stop() {
    pid=`ps -ef | grep '[p]ython proxy_core.py' | awk '{ print $2 }'`
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
    echo "Usage: /etc/init.d/hbproxy.sh {start|stop|restart}"
    exit 1
esac
exit 0
