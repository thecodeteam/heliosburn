#!/bin/bash
if [ "$EUID" != "0" ]
then
    echo "You must be the root user to run this installer."
    exit 1
fi

if [ -d /opt/HeliosBurn ]
then
    echo ">> Installing supervisord profiles under /etc/supervisor/conf.d/"
    install -b install/etc/supervisor/conf.d/*.conf /etc/supervisor/conf.d/
    echo ">> Setting up database - executing: 'python heliosburn/django/hbproject/create_db_model.py'"
    python heliosburn/django/hbproject/create_db_model.py
    echo ""
    echo "Installation complete - restart supervisord to load and run the Helios Burn components."
    exit 0
else
    echo "'/opt/HeliosBurn' does not exist! Ensure HeliosBurn is decompressed into /opt/ and re-run this."
    exit 1
fi

