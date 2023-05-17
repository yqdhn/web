from rest_framework import viewsets, status
from .serializers import *
from .model.models import *
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from django.db.models import Q
import uuid
import logging

class FlightList(APIView):
    def get(self, request):
        try:
            # filter flights and retern what is wanted
            flights = Flight.objects.filter(
                Q(departure_airport__name=request.data.get('departure_airport')) &
                Q(destination_airport__name=request.data.get('destination_airport')) &
                Q(departure_datetime=request.data.get('departure_datetime'))
            )

            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Flight.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

class FlightDetail(RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Flight.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

class PayBooking(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        psp_id = request.data.get('psp_id')
        try:
            # Ensure booking and psp exist
            booking = Booking.objects.get(id=kwargs.get('booking_id'))
            psp = PaymentProvider.objects.get(id=psp_id)

            # Create a id
            transaction_id = str(uuid.uuid4())

            return Response(transaction_id, status=status.HTTP_201_CREATED)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PaymentProvider.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

class BookFlight(APIView):
    def post(self, request):
        try:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                customer_data = serializer.validated_data.pop('customer')
                passport_number = customer_data.get('passport_number')
                # check if customer exist, if not create new customer
                try:
                    customer = Customer.objects.get(passport_number=passport_number)
                except Customer.DoesNotExist:
                    customer = Customer.objects.create(**customer_data)
                    customer.save()

                # Create and save the booking
                flight_id = serializer.validated_data.pop('flight')
                booking = Booking.objects.create(flight=flight_id, booking_status="on_hold", customer=customer, **serializer.validated_data)
                price = flight_id.price_per_seat
                booking.price = price
                booking.save()

                # Return the booking id, status, and price
                return Response({
                    'booking_id': booking.id,
                    'booking_status': booking.booking_status,
                    'price': booking.price,
                    'customer': CustomerSerializer(customer).data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

class GetBooking(APIView):
    def get(self, request, *args, **kwargs):
        try:
            booking = Booking.objects.get(id=kwargs.get('booking_id'))
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    def put(self, request, *args, **kwargs):
        try:
            booking = Booking.objects.get(id=kwargs.get('booking_id'))

            # Update departure_datetime
            departure_datetime = request.data.get('departure_datetime')
            if departure_datetime:
                booking.flight.departure_datetime = departure_datetime
                booking.flight.save()

            # Update customer details
            customer_data = request.data.get('customer')
            if customer_data:
                customer_id = customer_data.get('customer_id')
                if customer_id:
                    # Update customer
                    update_fields = {field: value for field, value in customer_data.items() if field != 'customer_id'}
                    Customer.objects.filter(id=customer_id).update(**update_fields)
                    
            return Response(status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

class ConfirmBooking(APIView):
    def put(self, request, *args, **kwargs):
        try:
            success_key = request.data.get('success_key')
            if success_key == 'confirmed' or success_key == "Confirmed":
                booking_id = request.data.get('booking_id')
                booking = Booking.objects.get(id=booking_id)
                booking.booking_status = 'confirmed'
                booking.save()

                tickets = Ticket.objects.filter(booking=booking)
                ticket_serializer = TicketSerializer(tickets, many=True)

                return Response({
                    'booking_id': booking.id,
                    'booking_status': booking.booking_status,
                    'tickets': ticket_serializer.data
                }, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
class CancelBooking(APIView):
    def put(self, request, *args, **kwargs):
        try:
            booking_id = request.data.get('booking_id')
            booking = Booking.objects.get(id=booking_id)
            booking.booking_status = 'cancelled'
            booking.save()

            return Response({
                'booking_id': booking.id,
                'booking_status': booking.booking_status
            }, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

class GetPSP(APIView):
    def get(self, request, *args, **kwargs):
        try:
            payment_providers = PaymentProvider.objects.all()
            serializer = PaymentProviderSerializer(payment_providers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
