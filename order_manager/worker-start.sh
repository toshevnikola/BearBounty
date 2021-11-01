#! /usr/bin/env bash
cd /order_manager && celery -A tasks.tasks worker -c 1 --pool gevent --loglevel=INFO