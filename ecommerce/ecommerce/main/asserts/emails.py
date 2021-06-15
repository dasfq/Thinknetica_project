from django.core.mail import EmailMultiAlternatives

def email_send(subject, text_content, from_email, to, html_content,reply_to):
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], reply_to)
    msg.attach_alternatives(html_content, 'text/html')
    msg.send(fail_silently=False)
