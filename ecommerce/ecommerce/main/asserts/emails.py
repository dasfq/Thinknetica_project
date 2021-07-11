from django.core.mail import EmailMultiAlternatives


def email_send(subject, text_content, from_email, to, html_content, reply_to):
    msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=to, reply_to=reply_to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send(fail_silently=False)
