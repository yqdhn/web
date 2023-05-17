"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .model.models import *
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/flight/<int:id>', FlightDetail.as_view(), name='flight-detail'),
    path('api/flights', FlightList.as_view(), name='flights'),
    path('api/paybooking/<int:booking_id>', PayBooking.as_view({'post': 'create'}), name='pay-booking'),
    path('api/book', BookFlight.as_view(), name='book-flight'),
    path('api/booking/<int:booking_id>', GetBooking.as_view(), name='get-booking'),
    path('api/confirmbooking', ConfirmBooking.as_view(), name='confirm-booking'),
    path('api/cancelbooking', CancelBooking.as_view(), name='cancel-booking'),
    path('api/paymentproviders', GetPSP.as_view(), name='payment-providers'),
]
