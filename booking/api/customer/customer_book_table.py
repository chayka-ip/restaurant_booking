from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from booking.services.helpers.customer_booking_helper import CustomerBookingHelper


class CustomerBookTableAPI(APIView):
    """
    'id': int - table id
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        helper = CustomerBookingHelper(self.request)
        return helper.customer_book_table()
