from django.db import models

class Aircraft(models.Model):
    tail_number = models.CharField(max_length=10)
    type = models.CharField(max_length=200)
    number_of_seats = models.CharField(max_length=10)

class Airport(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    time_zone = models.CharField(max_length=200)
    
class Flight(models.Model):
    flight_number = models.CharField(max_length=200)
    departure_airport = models.ForeignKey(Airport, related_name='departure_flights', on_delete=models.CASCADE)
    destination_airport = models.ForeignKey(Airport, related_name='arrival_flights', on_delete=models.CASCADE)
    departure_datetime = models.DateTimeField()
    duration = models.CharField(max_length=200)
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2)
    aircraft = models.ForeignKey(Aircraft, related_name="aircraft", on_delete=models.CASCADE)

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    date_of_birth = models.DateField()
    home_address = models.CharField(max_length=200, blank=True)
    allergies = models.CharField(max_length=200, blank=True)

class PaymentProvider(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    account_id = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_provider = models.ForeignKey(PaymentProvider, on_delete=models.CASCADE)
    BOOKING_STATUS_CHOICES = [
        ('on_hold', 'On Hold'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS_CHOICES, default='on_hold')

class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=200)
