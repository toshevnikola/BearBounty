#! /usr/bin/env bash
celery -A tasks.tasks worker -c 4 --pool gevent --loglevel=info