from django.db.models import QuerySet, Q
from rest_framework.response import Response
from rest_framework import status

from booking.models import RestaurantTable
from booking.serializers import (RestaurantTableCreateSerializer,
                                 RestaurantTableSerializer,
                                 CustomerTableFilter,
                                 CustomerTableFilterSerializer,
                                 RestaurantTablePublicSerializer)
from booking.services.helpers.base_model_helper import BaselHelper
from booking.services.error_formatter import ErrorFormatter
from booking.services.utils import try_get_int


class RestaurantTableHelper(BaselHelper):

    # ===== PUBLIC ACTIONS =====

    def get_filtered_table_list(self):
        default_filter = CustomerTableFilter()
        table_filter = CustomerTableFilterSerializer(default_filter,
                                                     data=self.request_data,
                                                     partial=True)

        if not table_filter.is_valid():
            error_text = table_filter.errors
            return ErrorFormatter(error_text=error_text,
                                  status=status.HTTP_400_BAD_REQUEST).as_response

        q_filter = table_filter.create(table_filter.validated_data)

        Q_available = Q(can_be_booked=True)
        Q_type = Q(table_type__icontains=q_filter.table_type)
        Q_seats = Q(seats__range=(q_filter.seats_min, q_filter.seats_max))
        Q_price = Q(price__range=(q_filter.price_min, q_filter.price_max))

        q: QuerySet = RestaurantTable.objects.filter(Q_available & Q_type & Q_seats & Q_price)

        serializer = RestaurantTablePublicSerializer(q, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ===== ADMIN ACTIONS =====

    def create_new_table(self):
        serializer = RestaurantTableCreateSerializer(data=self.request_data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        # create new instance
        serializer.save()

        data = {
            "detail": "New table created.",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def update_table(self):
        # Customer can't be changed here
        data = self.get_request_data_copy()
        customer_key = 'customer'
        if customer_key in data:
            data.pop(customer_key)

        table_id = try_get_int(data.get('id'))
        table_instance = RestaurantTable.objects.filter(id=table_id).first()
        if not table_instance:
            error_text = "Table with such 'id' is invalid or table does not exist."
            return ErrorFormatter(error_text=error_text,
                                  status=status.HTTP_400_BAD_REQUEST).as_response

        serializer = RestaurantTableSerializer(table_instance,
                                               data=data,
                                               partial=True)
        if serializer.is_valid():
            # update instance
            serializer.save()
            data = {
                "detail": "Table is updated.",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            error_text = serializer.errors
            return ErrorFormatter(error_text=error_text, status=status.HTTP_400_BAD_REQUEST).as_response
