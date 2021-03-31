import os
from datetime import datetime, timedelta

import requests
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Weather
from .serializers import CurrentWeatherSerializer, UserSerializer


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class CurrentWeatherApiView(CreateAPIView):
    serializer_class = CurrentWeatherSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = CurrentWeatherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lat = serializer.validated_data["lat"]
        long = serializer.validated_data["long"]
        detailing_type = serializer.validated_data["detailing_type"]
        try:
            relevance_time = timezone.now() - timedelta(seconds=int(os.environ.get("RELEVANCE_TIME")))
            obj = Weather.objects.get(updated_at__gt=relevance_time,
                                      lat=lat,
                                      long=long)
        except Weather.DoesNotExist:
            api_res = self.one_call_api(lat=lat, long=long)
            if not api_res:
                return Response({"data": {}}, status=status.HTTP_200_OK)
            obj, _ = Weather.objects.get_or_create(lat=lat, long=long)
            obj.data = api_res
            obj.save()
        if detailing_type is 0:
            data = obj.current
        if detailing_type is 1:
            data = obj.minutely
        if detailing_type is 2:
            data = obj.hourly
        if detailing_type is 3:
            data = obj.daily
        return Response(data=data, status=status.HTTP_200_OK)

    @staticmethod
    def one_call_api(lat, long):
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&appid={os.environ.get('OWM_KEY')}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {}
