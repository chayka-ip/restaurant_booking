from collections import namedtuple

MessageData = namedtuple("MessageData", "subject message")


def get_customer_success_booking_message(cancel_booking_link: str) -> MessageData:
    subject = 'Table booking'
    message = f'<html>\
                <body>\
                    <p>\
                        Dear customer!\
                    <br>\
                        Thank you for visiting out restaurant. Your booking will be accepted as soon as possible.\
                    <br>\
                        If you want to cancel your booking, please follow the \
                        <a href="{cancel_booking_link}" target="_blank">link</a>\
                    </p>\
                    <br>\
                    <br>\
                </body>\
                </html>'
    return MessageData(subject=subject, message=message)


def get_admin_accepted_booking_message() -> MessageData:
    subject = 'Your booking is accepted'
    message = 'Dear customer! Your booking is accepted.'
    return MessageData(subject=subject, message=message)


def get_admin_canceled_booking_message() -> MessageData:
    subject = 'Booking is canceled'
    message = 'Dear customer! Your booking was canceled.'
    return MessageData(subject=subject, message=message)


def get_booking_refused_message() -> MessageData:
    subject = 'Booking is refused'
    message = "Dear customer! Unfortunately, the table you've booked is already in use. Please select another one."
    return MessageData(subject=subject, message=message)

# def template ()-> MessageData:
#     subject = ''
#     message = ''
#     return MessageData(subject=subject, message=message)
