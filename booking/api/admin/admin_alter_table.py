from booking.api.admin.admin_base_api_view import AdminBaseAPIView
from booking.services.helpers.restaurant_table_helper import RestaurantTableHelper


class AdminAlterTableView(AdminBaseAPIView):
    """
        Endpoint to alter existing table

        'id' (required): int
        'table_type' (optional): regular | cabin | room
        'seats' (optional):  int
        'price' (optional): float
        'can_be_booked' (optional): bool

        'customer' - can't be changed explicitly here
    """

    def patch(self, request):
        helper = RestaurantTableHelper(request)
        return helper.update_table()
