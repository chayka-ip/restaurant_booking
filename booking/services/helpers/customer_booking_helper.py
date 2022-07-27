from rest_framework.response import Response
from rest_framework import status

from booking.models import (RestaurantTable,
                            CustomerBooking,
                            active_booking_status,
                            BookingStatus)
from booking.serializers import CustomerBookingSerializer
from booking.services.customer_booking_instance_from_request import CustomerBookingFromRequestData
from booking.services.helpers.base_model_helper import BaselHelper
from booking.services.error_formatter import ErrorFormatter
from booking.services.mail.mail_service import MailService
from booking.services.utils import try_get_int

class CustomerBookingHelper(BaselHelper):

    # ===== ADMIN ACTIONS =====

    def admin_get_active_bookings(self):
        query = CustomerBooking.objects.filter(status__in=active_booking_status)
        serializer = CustomerBookingSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def admin_accept_booking(self):
        data = CustomerBookingFromRequestData(request=self.request)
        if data.has_errors:
            return ErrorFormatter(error_text=data.error, status=data.status).as_response

        booking_instance = data.get_data()

        table_instance = booking_instance.table
        is_table_available = table_instance.can_be_booked
        if not is_table_available:
            table_id = booking_instance.table.id
            error_text = f'Decline booking. Table with id={table_id} is already booked.'
            return ErrorFormatter(error_text=error_text, status=status.HTTP_400_BAD_REQUEST).as_response

        # book table for this customer
        booking_instance.set_booked_status()
        table_instance.disable_for_booking(customer=booking_instance.customer)
        table_instance.refresh_from_db()

        booked_email = booking_instance.customer_email
        self.get_mail_service().send_email_on_admin_accepted_booking(email=booked_email)

        # decline all waiting bookings for this table
        booking_id = booking_instance.id
        other_bookings = CustomerBooking.objects.filter(table=table_instance,
                                                        status=BookingStatus.WAITING).exclude(id=booking_id)

        # obtain emails before query execution
        customers_query = other_bookings.select_related('customer').values_list('customer__email')
        refused_customers_email_list = [email[0] for email in customers_query]

        other_bookings.update(status=BookingStatus.REFUSED)

        self.get_mail_service().set_bulk_email_booking_decline(recipient_list=refused_customers_email_list)

        text = 'Table booking is accepted.'
        return Response({"detail": text}, status=status.HTTP_200_OK)

    def admin_cancel_booking(self):
        data = CustomerBookingFromRequestData(request=self.request)
        if data.has_errors:
            return ErrorFormatter(error_text=data.error, status=data.status).as_response

        booking_instance = data.get_data()
        table_instance = booking_instance.table
        is_active_booking = booking_instance.is_booked
        is_table_booked_by_this_user = booking_instance.customer == table_instance.customer

        if not is_active_booking:
            error_text = 'This booking was not accepted.'
            return ErrorFormatter(error_text=error_text, status=status.HTTP_400_BAD_REQUEST).as_response

        if is_table_booked_by_this_user:
            table_instance.enable_for_booking(clear_customer=True)

        booking_instance.set_canceled_status()

        email = booking_instance.customer_email
        self.get_mail_service().send_email_admin_canceled_booking(email=email)

        text = "Booking is canceled successfully."
        return Response({"detail": text})

    # ===== CUSTOMER ACTIONS =====

    def customer_book_table(self):
        table_id = try_get_int(self.request.GET.get('id'))
        table_instance = RestaurantTable.objects.filter(can_be_booked=True,
                                                        id=table_id).first()
        if not table_instance:
            error_text = f"This table can't be booked or does not exists."
            return ErrorFormatter(error_text=error_text, status=status.HTTP_400_BAD_REQUEST).as_response

        # finish booking procedure

        booking_instance = CustomerBooking.objects.filter(table=table_instance,
                                                          customer=self.user,
                                                          status__in=active_booking_status).first()

        if booking_instance:
            text = 'You have already booked this table. Please wait for the order confirmation.'
            return Response({"detail": text}, status=status.HTTP_200_OK)

        new_booking_instance: CustomerBooking = CustomerBooking.objects.create(table=table_instance,
                                                                               customer=self.user)

        email = self.get_user_email()
        cancel_booking_id = new_booking_instance.cancel_id

        self.get_mail_service().send_email_on_customer_booking(cancel_id=cancel_booking_id)

        success_text = f"Booking order is created successfully! " \
                       f"Please, check your email ({email}) for further instructions"
        return Response({"detail": success_text})

    def customer_cancel_booking(self):
        cancel_id: str = self.request.GET.get('id', '').replace(' ', '')
        booking_instance: CustomerBooking = CustomerBooking.objects.filter(cancel_id=cancel_id,
                                                                           status__in=active_booking_status).first()
        if not booking_instance:
            error_text = "This booking is invalid or can't be canceled."
            return ErrorFormatter(error_text=error_text, status=status.HTTP_400_BAD_REQUEST).as_response

        if booking_instance.is_waiting:
            booking_instance.set_canceled_status()
            text = "Your booking is canceled successfully."
            return Response({"detail": text})

        if booking_instance.is_booked:
            booking_instance.mark_as_waiting_for_booking_cancel()
            text = "Your request has been sent to the administrator. Please wait for further instructions."
            return Response({"detail": text})

    # ===== MAILING =====

    def get_mail_service(self) -> MailService:
        return MailService(self.request)
