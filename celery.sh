#!/bin/sh
# This script is to be used on a CentOS 7.5 production server which is running a shell-script.
cd /opt/django/smegurus-django/
source env/bin/activate
exec celery --app=smegurus.celery:app worker --loglevel=INFO -n worker.%%h
