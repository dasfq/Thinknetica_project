from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import CustomUser, Profile, Subscriber, TicketItem
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from main.asserts.emails import email_send


@receiver(post_save, sender = CustomUser, dispatch_uid = 'signal_1')
def default_group(sender, instance, **kwargs):
    group, is_created = Group.objects.get_or_create(name='Common Users')
    instance.groups.add(group)


@receiver(post_save, sender = Profile, dispatch_uid = 'signal_2')
def default_group(sender, instance, **kwargs):
    group, is_created = Group.objects.get_or_create(name='Common Users')
    instance.groups.add(group)

@receiver(post_save, sender = settings.AUTH_USER_MODEL, dispatch_uid = 'signal_3')
def send_hello_email(sender, instance, **kwargs):
    """Sending of hello email"""
    subject = 'Спасибо за регистрацию!'
    text_content = f"{instance}, приветствуем на нашем сайте!"
    html_content = '<p><strong>Welcome</strong> to the best site ever!</p>'
    from_email = "from@mail.com"
    reply_to = [from_email]
    to = [instance.email]
    email_send(
        subject,
        text_content,
        from_email,
        to,
        html_content,
        reply_to,
    )

# @receiver(post_save, sender = TicketItem)
# def send_newsletter(sender, instance, created, **kwargs):
#     """Рассылка при создании нового объявления  """
#     if created:
#         to = [profile.profile.email for profile in Subscriber.objects.filter(is_active=True)]
#         ticket_name = instance
#         price = instance.price
#         qty = instance.qty
#         condition = instance.state
#         tags = list(instance.tag.all())
#         subject = 'Новые объявления на нашем сайте!'
#         text_content = f"{instance}, ознакомьтесь с новыми объявлениями на нашем сайте!"
#         html_content = f'<p><strong>{ticket_name}</strong></p><p>Цена:</p>{price}</p><p>Состояние: {condition}</p>'
#         from_email = "from@mail.com"
#         reply_to = [from_email]
#         email_send(
#             subject,
#             text_content,
#             from_email,
#             to,
#             html_content,
#             reply_to
#         )



