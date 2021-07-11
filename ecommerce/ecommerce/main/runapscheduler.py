# from django.conf import settings
# import logging
# from main.asserts.emails import email_send
# import datetime
# from main.models import Subscriber, TicketCar
# from django.template.loader import render_to_string
#
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.combining import AndTrigger
# from apscheduler.triggers.interval import IntervalTrigger
# from apscheduler.triggers.cron import CronTrigger
# from django.core.management.base import BaseCommand
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
# from django_apscheduler import util
#
# logger = logging.basicConfig(level=logging.DEBUG)
#
# def weekly_send():
#     """Sending of weekly newsletter with new tickets"""
#     now = datetime.datetime.now()
#     start_period = now - datetime.timedelta(days=7)
#     tickets_list = TicketCar.objects.filter(date_created__gte==start_period)
#     to = [profile.profile.email for profile in Subscriber.objects.filter(is_active=True)]
#     subject = 'Weekly newsletter for new car tickets'
#     text_content = 'Please take a look at our new cars tickets!'
#     from_email = ["admin@mail.ru"]
#     reply_to = ["admin@mail.ru"]
#     context = {
#         "tickets": tickets_list,
#     }
#     html_content = render_to_string('newsletters/new_cars.html', context)
#
#     if tickets_list:
#         email_send(subject, text_content, from_email, to, html_content,reply_to)
#
#
# @util.close_old_connections
# def delete_old_job_executions(max_age=604_800):
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs APScheduler."
#     trigger = AndTrigger([IntervalTrigger(days=7), CronTrigger(day_of_week='mon')])
#
#     def handle(self):
#         scheduler = BackgroundScheduler()
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#         scheduler.add_job(
#             weekly_send,
#             trigger=self.trigger,
#             id='weekly_newsletter',
#             max_instances=1,
#             replace_existing=True
#         )
#         logger.info("added job: weekly newsletter of item tickets")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(day_of_week='sun', hour="23", minute="50"),
#             replace_existing=True,
#             max_instances=1,
#             id='delete_old_jobs'
#         )
#         logger.info("Added weekly job: 'delete_old_jobs'.")
#
#         try:
#             logger.info("starting of scheduler")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info('Keyboard interrupted.')
#             scheduler.shutdown()
#             logger.info('Scheduler is shutted down successfully')
