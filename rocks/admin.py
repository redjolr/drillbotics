from django.contrib import admin

from .models import Rock, Material, RockComposition

admin.site.register(Rock)
admin.site.register(Material)
admin.site.register(RockComposition)
