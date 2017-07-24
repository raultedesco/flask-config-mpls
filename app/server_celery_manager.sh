#!/bin/bash
celery -A tasks_list.celery worker --loglevel=info