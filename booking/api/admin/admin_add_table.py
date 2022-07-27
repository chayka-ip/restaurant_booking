from booking.api.admin.admin_base_api_view import AdminBaseAPIView
from booking.services.helpers.restaurant_table_helper import RestaurantTableHelper


class AdminAddTableView(AdminBaseAPIView):
    """
        'table_type' (optional): "regular" | "cabin" | "room"
        'seats' (optional):  int
        'price' (optional): float
        'can_be_booked' (optional): bool
    """

    def post(self, request):
        helper = RestaurantTableHelper(request)
        return helper.create_new_table()
