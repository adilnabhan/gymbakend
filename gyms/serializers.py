from rest_framework import serializers
from .models import Gym


class GymListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = [
            'id', 'name', 'slug', 'city', 'state', 'rating',
            'monthly_fee', 'categories', 'amenities', 'latitude', 'longitude',
        ]


class GymDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'
