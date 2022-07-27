from django.conf import settings

from booking.services.helpers.base_model_helper import BaselHelper
from booking.services.mail.mail_sender import MailSender
from booking.services.mail.mail_text_generator import (get_customer_success_booking_message,
                                                       get_admin_canceled_booking_message,
                                                       get_admin_accepted_booking_message,
                                                       get_booking_refused_message
                                                       )
from booking.services.mail.tasks import send_mail_async
from booking.services.utils import generate_customer_cancel_booking_link

IS_MAILING_ENABLED = settings.ENABLE_MAILING


class MailService(BaselHelper):
    def __init__(self, request, is_async_send=True):
        super().__init__(request)
        self.is_async_send = is_async_send

    def send(self, sender: MailSender):
        if IS_MAILING_ENABLED:
            if self.is_async_send:
                send_mail_async.delay(sender)
            else:
                sender.send()

    def send_email_on_customer_booking(self, cancel_id: str):
        cancel_link = generate_customer_cancel_booking_link(request=self.request, cancel_id=cancel_id)
        email = self.get_user_email()
        message_data = get_customer_success_booking_message(cancel_booking_link=cancel_link)
        sender = MailSender(subject=message_data.subject,
                            message=message_data.message,
                            recipient=email,
                            is_html=True)
        self.send(sender)

    def send_email_on_admin_accepted_booking(self, email: str):
        message_data = get_admin_accepted_booking_message()
        sender = MailSender(subject=message_data.subject,
                            message=message_data.message,
                            recipient=email)
        self.send(sender)

    def send_email_admin_canceled_booking(self, email: str):
        message_data = get_admin_canceled_booking_message()
        sender = MailSender(subject=message_data.subject,
                            message=message_data.message,
                            recipient=email)
        self.send(sender)

    def set_bulk_email_booking_decline(self, recipient_list: list):
        message_data = get_booking_refused_message()
        sender = MailSender(subject=message_data.subject,
                            message=message_data.message,
                            recipient_list=recipient_list)
        self.send(sender)
