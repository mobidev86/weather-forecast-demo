from django.contrib import admin

# Register your models here.
from core.models import Weather


class WeatherAdmin(admin.ModelAdmin):
    list_display = ('id', 'lat', 'long', 'created_at', 'updated_at')


admin.site.register(Weather, WeatherAdmin)
