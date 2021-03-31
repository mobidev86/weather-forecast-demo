from django.contrib.postgres.fields import JSONField
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Weather(TimestampedModel):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    data = JSONField(default=dict)

    def __str__(self):
        return f"{self.lat} {self.long}"

    def specific_data(self, attrib):
        return {
            "lat": self.data['lat'],
            "lon": self.data['lon'],
            "timezone": self.data['timezone'],
            "timezone_offset": self.data['timezone_offset'],
            attrib: self.data.get(attrib)
        }

    @property
    def minutely(self):
        if type(self.data) is dict and 'minutely' in self.data:
            return self.specific_data('minutely')

    @property
    def hourly(self):
        if type(self.data) is dict and 'hourly' in self.data:
            return self.specific_data('hourly')

    @property
    def daily(self):
        if type(self.data) is dict and 'daily' in self.data:
            return self.specific_data('daily')

    @property
    def current(self):
        if type(self.data) is dict and 'current' in self.data:
            return self.specific_data('current')
