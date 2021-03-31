import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.views import CurrentWeatherApiView


# Create your tests here.
class WeatherApiTest(APITestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        user, _ = User.objects.get_or_create(username='test')
        self.token, _ = Token.objects.get_or_create(user=user)
        self.valid_payload = {"detailing_type": 1, "lat": "23.022500", "long": "72.571400"}
        self.invalid_payload = {}

    def api_call(self, valid_payload):
        response = self.client.post(
            reverse('get-weather-info'),
            data=json.dumps(valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        result = CurrentWeatherApiView.one_call_api(lat=valid_payload["lat"], long=valid_payload["long"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["timezone"], result["timezone"])
        self.assertEqual(response.json()["timezone_offset"], result["timezone_offset"])
        self.assertEqual(response.json()["lat"], result["lat"])
        self.assertEqual(response.json()["lon"], result["lon"])
        return response, result

    def test_valid_minutely_weather_value(self):
        response, result = self.api_call(self.valid_payload)
        self.assertEqual(response.json()["minutely"], result["minutely"])

    def test_valid_hourly_value(self):
        valid_payload = {"detailing_type": 2, "lat": "23.022500", "long": "72.571400"}
        response, result = self.api_call(valid_payload)
        self.assertEqual(response.json()["hourly"], result["hourly"])

    def test_valid_daily_value(self):
        valid_payload = {"detailing_type": 3, "lat": "23.022500", "long": "72.571400"}
        response, result = self.api_call(valid_payload)
        self.assertEqual(response.json()["daily"], result["daily"])

    def test_valid_current_value(self):
        valid_payload = {"detailing_type": 0, "lat": "23.022500", "long": "72.571400"}
        response, result = self.api_call(valid_payload)
        self.assertEqual(response.json()["current"], result["current"])

    def test_create_invalid_puppy(self):
        response = self.client.post(
            reverse('get-weather-info'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'detailing_type': ['This field is required.'],
                                           'lat': ['This field is required.'],
                                           'long': ['This field is required.']})
