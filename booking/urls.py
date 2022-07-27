from django.urls import path
from rest_framework.reverse import reverse
from .api.admin import (admin_alter_table,
                        admin_accept_booking,
                        admin_add_table,
                        admin_cancel_booking,
                        admin_get_active_bookings)

from .api.customer import (customer_book_table,
                           customer_view_tables,
                           customer_cancel_booking)

app_name = 'booking'

customer_cancel_booking_api_name = 'customer-cancel-booking'

admin_urls = [
    path('admin/add_table/', admin_add_table.AdminAddTableView.as_view()),
    path('admin/update_table/', admin_alter_table.AdminAlterTableView.as_view()),
    path('admin/accept_booking/', admin_accept_booking.AdminAcceptBookingAPI.as_view()),
    path('admin/cancel_booking/', admin_cancel_booking.AdminCancelBookingAPI.as_view()),
    path('admin/view_active_bookings/', admin_get_active_bookings.AdminGetActiveBookingsAPI.as_view()),
]

customer_urls = [
    path('customer/view_tables/', customer_view_tables.CustomerListTables.as_view()),
    path('customer/book_table/', customer_book_table.CustomerBookTableAPI.as_view()),
    path('customer/cancel_booking/', customer_cancel_booking.CustomerCancelBookingAPI.as_view(),
         name=customer_cancel_booking_api_name),
]

urlpatterns = admin_urls + customer_urls


def get_customer_discard_booking_api(request):
    return reverse(f'{app_name}:{customer_cancel_booking_api_name}', request=request)
