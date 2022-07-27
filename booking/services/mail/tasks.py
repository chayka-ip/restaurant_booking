from celery import shared_task

from booking.services.mail.mail_sender import MailSender


@shared_task
def send_mail_async(sender: MailSender):
    sender.send()

