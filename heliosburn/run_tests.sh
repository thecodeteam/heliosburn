#!/bin/bash

ps aux | egrep -q "[p]ython -u.*hblog\.py"
if [ $? -ne 0 ]
then
    echo "!!! hblog must be online to proceed with tests."
    exit 1
fi

CWD=$(pwd)  # preserve cdw

#Run Django tests
TESTS="Django API unittest"
cd django/hbproject
python manage.py test api
if [ $? -ne 0 ]
then
    echo "!!! Failed tests for: $TESTS"
    exit 1
else
    echo ">>> Tests OK for $TESTS"
fi

TESTS="Django WEBUI unittest"
cd django/hbproject
python manage.py test webui
if [ $? -ne 0 ]
then
    echo "!!! Failed tests for: $TESTS"
    exit 1
else
    echo ">>> Tests OK for $TESTS"
fi


#Run Proxy tests
cd $CWD
TESTS="Proxy unittest"
python -m unittest proxy
if [ $? -ne 0 ]
then
    echo "!!! Failed tests for: $TESTS"
    exit 1
else
    echo ">>> Tests OK for $TESTS"
fi

#Run Proxy module tests
cd $CWD
TESTS="Proxy modules unittest"
python -m unittest proxy/modules
if [ $? -ne 0 ]
then
    echo "!!! Failed tests for: $TESTS"
    exit 1
else
    echo ">>> Tests OK for $TESTS"
fi

