from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from booking.services.helpers.customer_booking_helper import CustomerBookingHelper


class CustomerCancelBookingAPI(APIView):
    """
    Customer sends his discard key from booking letter to discard his booking.
    If booking has been accepted by the administrator - we notify them about this issue.
    Else: discard booking.

    'id': str
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        helper = CustomerBookingHelper(self.request)
        return helper.customer_cancel_booking()
