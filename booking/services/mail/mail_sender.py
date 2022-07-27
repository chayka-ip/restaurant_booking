from django.core.mail import send_mail
from django.conf import settings


def _get_recipient_list(recipient, recipient_list: list):
    if not recipient_list:
        recipient_list = []
    if recipient not in recipient_list:
        recipient_list.append(recipient)
    return recipient_list


class MailSender:
    """
    Simple wrapper to send mail.
    Single or many recipients can be specified.
    """

    def __init__(self, subject: str, message: str, recipient=None, recipient_list: list = None, is_html=False,
                 send_now=True):
        self.from_email = settings.EMAIL_HOST_USER
        self.subject = subject
        self.message = message
        self.is_html=is_html
        self.recipient_list = _get_recipient_list(recipient, recipient_list)

        if send_now:
            self.send()

    def send(self):
        d = {'subject': self.subject,
             'from_email': self.from_email,
             'recipient_list': self.recipient_list,
             'message': '',
             'fail_silently': True}
        if self.is_html:
            d['html_message'] = self.message
        else:
            d['message'] = self.message

        send_mail(**d)
