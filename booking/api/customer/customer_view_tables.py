from rest_framework.views import APIView
from booking.services.helpers.restaurant_table_helper import RestaurantTableHelper


class CustomerListTables(APIView):

    def post(self, request):
        """ Request can contain all possible search fields or some of them """
        helper = RestaurantTableHelper(self.request)
        return helper.get_filtered_table_list()
