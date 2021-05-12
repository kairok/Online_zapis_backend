from django.contrib import admin
from .models import *



admin.site.register(Client)
admin.site.register(Master)
admin.site.register(Workcalendar)
admin.site.register(Zapis)
admin.site.register(Spec)
admin.site.register(Workday)

admin.site.register(Firma)

admin.site.register(UserProfile)
admin.site.register(Accounting)