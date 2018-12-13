from __future__ import absolute_import
from celery import Celery

from geoworker import BROKER_URL

app = Celery('geoworker', broker=BROKER_URL, include=['geoworker.tasks'])
