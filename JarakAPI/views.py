from django.shortcuts import render
from .models import Product, Profile
from django.contrib.auth.models import User
from .serializers import  ProductSerializer, ProfileSerializer, ProfileUpdateSerializer, CreateProductSerializer, UserCreateSerializer, RentedSerializer
from .permissions import IsProductOwner

# DRF Imports:
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser


class Register(CreateAPIView):
    serializer_class = UserCreateSerializer


class ProductList(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProfileDetails(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ProfileUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'profile_id'


class Update(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'


class Create(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CreateRent(CreateAPIView):
    serializer_class = RentedSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.profile)


class Delete(DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsProductOwner]
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'

