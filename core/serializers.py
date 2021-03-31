from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CurrentWeatherSerializer(serializers.Serializer):
    detailing_type = serializers.ChoiceField(
        choices=[(0, "Current weather"), (1, "Minute forecast for 1 hour"),
                 (2, "Hourly forecast for 48 hours"), (3, "Daily forecast for 7 days")]
    )
    lat = serializers.FloatField()
    long = serializers.FloatField()
