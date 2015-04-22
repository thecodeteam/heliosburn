#!/bin/sh
if [ -d /opt/HeliosBurn ]
then
    install -b heliosburn/supervisord_conf_d/*.conf /etc/supervisor/conf.d/
    exit 0
else
    echo "'/opt/HeliosBurn' does not exist! Ensure HeliosBurn is decompressed into /opt/ and re-run this."
    exit 1
fi
