from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from booking.models import RestaurantTable, TableType, CustomerBooking


class RestaurantTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTable
        fields = ('id',
                  'table_type',
                  'seats',
                  'can_be_booked',
                  'price',
                  'customer_email',
                  'created',
                  )


class RestaurantTablePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTable
        fields = ('id',
                  'table_type',
                  'seats',
                  'price',
                  )


class RestaurantTableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTable
        fields = (
            'table_type', 'seats', 'can_be_booked', 'price'
        )


class CustomerTableFilter:
    def __init__(self, table_type: str = '',
                 seats_min: int = RestaurantTable.SEATS_MIN,
                 seats_max: int = RestaurantTable.SEATS_MAX,
                 price_min: int = RestaurantTable.PRICE_MIN,
                 price_max: int = RestaurantTable.PRICE_MAX):
        self.table_type = table_type
        self.seats_min = seats_min
        self.seats_max = seats_max
        self.price_min = price_min
        self.price_max = price_max


class CustomerTableFilterSerializer(serializers.Serializer):
    # table_type can have any type from TableType.choices and empty string to exclude this filter parameter
    table_type = serializers.ChoiceField(choices=TableType.choices)
    seats_min = serializers.IntegerField(default=RestaurantTable.SEATS_MIN,
                                         validators=[
                                             MinValueValidator(RestaurantTable.SEATS_MIN),
                                             MaxValueValidator(RestaurantTable.SEATS_MAX)
                                         ])
    seats_max = serializers.IntegerField(default=1,
                                         validators=[
                                             MinValueValidator(RestaurantTable.SEATS_MIN),
                                             MaxValueValidator(RestaurantTable.SEATS_MAX)
                                         ])
    price_min = serializers.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         validators=[
                                             MinValueValidator(RestaurantTable.PRICE_MIN),
                                             MaxValueValidator(RestaurantTable.PRICE_MAX)
                                         ])
    price_max = serializers.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         validators=[
                                             MinValueValidator(RestaurantTable.PRICE_MIN),
                                             MaxValueValidator(RestaurantTable.PRICE_MAX)
                                         ])

    def update(self, instance, validated_data):
        if not isinstance(instance, CustomerTableFilter):
            return
        instance.table_type = validated_data.get('table_type', instance.table_type)
        instance.seats_min = validated_data.get('seats_min', instance.seats_min)
        instance.seats_max = validated_data.get('seats_max', instance.seats_max)
        instance.price_min = validated_data.get('price_min', instance.price_min)
        instance.price_max = validated_data.get('price_max', instance.price_max)

    def create(self, validated_data):
        return CustomerTableFilter(**validated_data)


class CustomerBookingSerializer(serializers.ModelSerializer):
    table = RestaurantTableSerializer(read_only=True)

    class Meta:
        model = CustomerBooking
        fields = ('id', 'table', 'customer_email', 'status', 'is_waiting_for_discard')
