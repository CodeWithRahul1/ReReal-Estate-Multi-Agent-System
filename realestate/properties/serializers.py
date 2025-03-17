from rest_framework import serializers
from .models import Property, Booking


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'property', 'visit_date', 'visit_time', 'status']
