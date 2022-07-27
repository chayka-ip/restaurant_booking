from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

import uuid


def _generate_discard_id():
    return str(uuid.uuid4())


class TableType(models.TextChoices):
    REGULAR = 'regular'  # обычный столик
    CABIN = 'cabin'  # столик кабинного типа
    ROOM = 'room'  # столик в отдельной комнате


class BookingStatus(models.TextChoices):
    BOOKED = 'booked'
    WAITING = 'waiting'
    REFUSED = 'refused'
    CANCELED = 'canceled'


active_booking_status = [BookingStatus.WAITING, BookingStatus.BOOKED]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True,
                             blank=True,
                             null=True)
    username = models.CharField(unique=True,
                                max_length=255)
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    def __repr__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class RestaurantTable(models.Model):
    """" Contains all tables for the restaurant"""
    SEATS_MIN = 1
    SEATS_MAX = 100
    PRICE_MIN = 0
    PRICE_MAX = 99999

    table_type = models.CharField(max_length=100,
                                  choices=TableType.choices,
                                  default=TableType.REGULAR)

    seats = models.PositiveSmallIntegerField(default=SEATS_MIN,
                                             validators=[
                                                 MinValueValidator(SEATS_MIN),
                                                 MaxValueValidator(SEATS_MAX)
                                             ])

    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                validators=[
                                    MinValueValidator(PRICE_MIN),
                                    MaxValueValidator(PRICE_MAX)])

    can_be_booked = models.BooleanField(default=True)
    customer = models.ForeignKey(CustomUser,
                                 on_delete=models.CASCADE,
                                 related_name='booking',
                                 null=True,
                                 blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def customer_email(self):
        if self.customer:
            return self.customer.email
        return ''

    def __repr__(self):
        return f'{self.customer_email} | type: {self.table_type} | seats: {self.seats} | ' \
               f'price: {self.price} | can_be_booked: {self.can_be_booked}'

    def enable_for_booking(self, clear_customer=True):
        self.can_be_booked = True
        if clear_customer:
            self.customer = None
        self.save()

    def disable_for_booking(self, customer=None):
        self.can_be_booked = False
        if customer:
            self.customer = customer
        self.save()


class CustomerBooking(models.Model):
    """
    This model contains information about booking requests.

    is_waiting_for_cancel - flag to show that customer wants to cancel his booking
    when his booking has been accepted
    """
    table = models.ForeignKey(RestaurantTable,
                              on_delete=models.CASCADE,
                              related_name='booking')
    customer = models.ForeignKey(CustomUser,
                                 on_delete=models.CASCADE,
                                 related_name='user_booking')
    status = models.CharField(max_length=15,
                              default=BookingStatus.WAITING,
                              choices=BookingStatus.choices)
    cancel_id = models.CharField(max_length=36,
                                 unique=True,
                                 editable=False,
                                 default=_generate_discard_id)
    is_waiting_for_cancel = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def customer_email(self):
        return self.customer.email

    @property
    def is_waiting(self):
        return self.status == BookingStatus.WAITING

    @property
    def is_booked(self):
        return self.status == BookingStatus.BOOKED

    def set_booked_status(self):
        self.status = BookingStatus.BOOKED
        self.save()

    def set_canceled_status(self):
        self.status = BookingStatus.CANCELED
        self.save()

    def mark_as_waiting_for_booking_cancel(self):
        self.is_waiting_for_cancel = True
        self.save()
