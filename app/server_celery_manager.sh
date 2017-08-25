#!/bin/bash
#celery -A tasks_list.celery worker -l info --logfile=/var/log/celery/%n%I.log
celery -A tasks_list.celery worker --loglevel=INFO



