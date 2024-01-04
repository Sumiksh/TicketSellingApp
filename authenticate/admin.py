from django.contrib import admin
from .models import Concert
from .models import ConcertSeat
from .models import Venue

# Register your models here.

admin.site.register(Concert)
admin.site.register(ConcertSeat)
admin.site.register(Venue)