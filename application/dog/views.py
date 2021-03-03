from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Breed, Dog

from dog import serializers
from core.paginations import CustomLimitOffSetPagination, \
                             CustomPageNumberPagination


class BreedViewSet(viewsets.ModelViewSet):
    """Manage Breed in the database"""
    queryset = Breed.objects.all()
    serializer_class = serializers.BreedSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomLimitOffSetPagination

    def get_queryset(self):
        queryset = Breed.objects.all()

        param_name = self.request.GET.get('name')
        if param_name:
            queryset = queryset.filter(name=param_name)
        return queryset


class DogViewSet(viewsets.ModelViewSet):
    """Manage Dog in the database"""
    queryset = Dog.objects.all().order_by('-id')
    serializer_class = serializers.DogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Dog.objects.all().order_by('-id')

        param_name = self.request.GET.get('name')
        param_breed = self.request.GET.get('breed')

        if param_name:
            queryset = queryset.filter(name=param_name)
        elif param_breed:
            breed = Breed.objects.get(name=param_breed)
            queryset = queryset.filter(breed=breed)
        else:
            param_breed = self.request.GET.get('breed_name')
            if param_breed:
                breed = Breed.objects.get(name=param_breed)
                queryset = queryset.filter(breed=breed)

        return queryset
