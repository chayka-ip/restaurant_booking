from rest_framework import status
from booking.models import CustomerBooking
from booking.services.data_or_error_from_request import DataOrErrorFromRequestData
from booking.services.utils import try_get_int


class CustomerBookingFromRequestData(DataOrErrorFromRequestData):

    def _extract(self) -> [CustomerBooking, None]:
        customer_booking_id = try_get_int(self.request.GET.get('id'))
        self.data = CustomerBooking.objects.filter(id=customer_booking_id).first()

        if not self.data:
            self.error = f'This booking does not exists'
            self.status = status.HTTP_400_BAD_REQUEST

    def get_data(self) -> CustomerBooking:
        return self.data
