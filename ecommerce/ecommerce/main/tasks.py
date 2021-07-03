from __future__ import absolute_import, unicode_literals

# Это позволит убедиться, что приложение всегда импортируется, когда запускается Django
from celery import shared_task
from .celery import app
import time

@shared_task
def add(x,y):
    return x+y


@app.task
def test():
    time.sleep(7)
    print("3d task before 1st")


@app.task
def test():
    time.sleep(2)
    print("1st task")


@app.task
def test():
    time.sleep(5)
    print("2st task")

