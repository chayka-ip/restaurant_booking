from booking.api.admin.admin_base_api_view import AdminBaseAPIView
from booking.services.helpers.customer_booking_helper import CustomerBookingHelper


class AdminCancelBookingAPI(AdminBaseAPIView):
    """
    Endpoint for booking canceling.

    'id': int - customer booking id
    """

    def post(self, request):
        helper = CustomerBookingHelper(request)
        return helper.admin_cancel_booking()
