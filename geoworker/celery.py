from __future__ import absolute_import
from celery import Celery

from geoworker import RABBIT_MQ_URL

app = Celery('geoworker',
             broker=RABBIT_MQ_URL,
             include=['geoworker.tasks'])
