from __future__ import absolute_import, unicode_literals

# Это позволит убедиться, что приложение всегда импортируется, когда запускается Django
from celery import shared_task
from ecommerce.celery import app
# from celery import Celery
# from celery.schedules import crontab
import time
import datetime
from main.asserts.emails import email_send
from main.models import TicketCar, Subscriber
import json


@shared_task
def add(x,y):
    print(x+y)
    return x+y


@shared_task
def test3():
    time.sleep(7)
    print("3d task before 1st")


@app.task
def test1():
    time.sleep(2)
    print("1st task")


@app.task
def test2():
    time.sleep(5)
    print("2st task")

@shared_task
def weekly_send():
    """Sending of weekly newsletter with new tickets"""
    now = datetime.datetime.now()
    start_period = now - datetime.timedelta(days=7)
    tickets_list = TicketCar.objects.filter(date_created__gte==start_period)
    to = [profile.profile.email for profile in Subscriber.objects.filter(is_active=True)]
    subject = 'Weekly newsletter for new car tickets'
    text_content = 'Please take a look at our new cars tickets!'
    from_email = ["admin@mail.ru"]
    reply_to = ["admin@mail.ru"]
    context = {
        "tickets": tickets_list,
    }
    html_content = render_to_string('newsletters/new_cars.html', context)

    if tickets_list:
        email_send(subject, text_content, from_email, to, html_content,reply_to)

@shared_task
def send_notification(instance):
    """Уведомление при создании нового объявления  """
    to = [profile.profile.email for profile in Subscriber.objects.filter(is_active=True)]
    ticket_name = instance['name']
    price = instance["price"]
    condition = instance["state"]
    subject = 'Новые объявления на нашем сайте!'
    text_content = f"Привет, ознакомьтесь с новыми объявлениями на нашем сайте!"
    html_content = f'<p><strong>{ticket_name}</strong></p><p>Цена:</p>{price}</p><p>Состояние: {condition}</p>'
    from_email = "from@mail.com"
    reply_to = [from_email]
    email_send(
        subject,
        text_content,
        from_email,
        to,
        html_content,
        reply_to
    )