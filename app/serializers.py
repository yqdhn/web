from rest_framework import serializers
from .model.models import Aircraft, Airport, Flight, Customer, PaymentProvider, Booking, Ticket

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer(read_only=True)
    destination_airport = AirportSerializer(read_only=True)
    aircraft = AircraftSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PaymentProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    
    class Meta:
        model = Booking
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
