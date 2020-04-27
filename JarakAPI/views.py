from django.shortcuts import render
from .models import Product, Profile
from django.contrib.auth.models import User
from .serializers import  ProductSerializer, ProfileSerializer, ProfileUpdateSerializer, CreateProductSerializer, UserCreateSerializer, UserLoginSerializer
# DRF Imports:
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
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
		return self.request.user.profile

class ProfileUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'profile_id'

class Update(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'

class Create(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class Delete(DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'
