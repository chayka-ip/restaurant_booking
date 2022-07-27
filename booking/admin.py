from django.contrib import admin

# Register your models here.
from booking.models import RestaurantTable, CustomerBooking, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'first_name', 'last_name', 'is_staff')
    readonly_fields = ('id',)


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_type', 'seats', 'can_be_booked', 'price', 'customer_email', 'created')
    readonly_fields = ('id', 'created', 'customer_email')


@admin.register(CustomerBooking)
class CustomerBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_id', 'customer', 'status', 'cancel_id')
    readonly_fields = ('id',)

    def get_table_id(self, obj: CustomerBooking):
        if obj.table:
            return obj.table.id
