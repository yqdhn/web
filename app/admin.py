from django.contrib import admin
from .model.models import *

admin.site.register(Aircraft)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Customer)
admin.site.register(PaymentProvider)
admin.site.register(Booking)
admin.site.register(Ticket)