from booking.api.admin.admin_base_api_view import AdminBaseAPIView
from booking.services.helpers.customer_booking_helper import CustomerBookingHelper


class AdminAcceptBookingAPI(AdminBaseAPIView):
    """
    Endpoint for booking acceptance.

    'id': int - customer booking id
    """

    def post(self, request):
        helper = CustomerBookingHelper(self.request)
        return helper.admin_accept_booking()
