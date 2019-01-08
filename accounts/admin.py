from django.contrib import admin

from .models import Specialization, Occupation, SpecificOccupation

admin.site.register(Specialization)
admin.site.register(Occupation)
admin.site.register(SpecificOccupation)
