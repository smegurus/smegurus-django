#!/bin/csh
# This script is to be used on a FreeBSD production server which is running a C-shell.
cd /usr/home/django/smegurus-django/
source env/bin/activate.csh
exec celery --app=smegurus.celery:app worker --loglevel=INFO -n worker.%%h
