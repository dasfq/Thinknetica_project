from __future__ import absolute_import, unicode_literals

# Это позволит убедиться, что приложение всегда импортируется, когда запускается Django
from celery import shared_task

@shared_task
def add(x,y):
    return x+y