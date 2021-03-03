from rest_framework import serializers

from core.models import Breed, Dog


class BreedSerializer(serializers.ModelSerializer):
    """Serializer for Breed Objects"""

    class Meta:
        model = Breed
        fields = ('id', 'name')
        read_only_fields = ('id',)


class DogSerializer(serializers.ModelSerializer):
    """Serializer for Dog Objects"""

    class Meta:
        model = Dog
        fields = ('id', 'name', 'breed')
        read_only_fields = ('id',)
