"""
Файл настроек Celery
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# этот код скопирован с manage.py
# он установит модуль настроек по умолчанию Django для приложения 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# здесь вы меняете имя
app = Celery("ecommerce")

# Для получения настроек Django, связываем префикс "CELERY" с настройкой celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# загрузка tasks.py из всех приложений проекта
app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_periodic_task(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(day_of_week=1, hour=12, minute=0),
#         main.weekly_send.s(),
#         name='weekly_newsletter'
#     )
#     sender.add_periodic_task(10.0, add.s(3,5), name='test task')

app.conf.beat_schedule = {
    'random_name': {
        'task': "main.tasks.add",
        "schedule": 10.0,
        "args": (15,10)
    },
    "send_weekly_newsletter": {
        "task": "main.tasks.weekly_send",
        "schedule": crontab(day_of_week=1, hour=12, minute=0)
    }
}