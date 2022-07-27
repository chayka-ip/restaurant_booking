from booking.api.admin.admin_base_api_view import AdminBaseAPIView
from booking.services.helpers.customer_booking_helper import CustomerBookingHelper


class AdminGetActiveBookingsAPI(AdminBaseAPIView):

    def get(self, request):
        helper = CustomerBookingHelper(self.request)
        return helper.admin_get_active_bookings()
