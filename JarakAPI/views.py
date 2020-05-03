from django.shortcuts import render
from .models import Product, Profile, RentedItem
from django.contrib.auth.models import User
from .serializers import  ProductSerializer, RentedListSerializer, ProfileSerializer, ProfileUpdateSerializer, CreateProductSerializer, UserCreateSerializer, RentedSerializer, ReturnSerializer
from .permissions import IsProductOwner
from datetime import datetime

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

class ProductOwnerProfile(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'profile_id'

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
        serializer.save(owner=self.request.user.profile)

#--------------------------Rent related views----------------------------------------------------------------------------
class RentList(ListAPIView):
    serializer_class = RentedListSerializer
    queryset = RentedItem.objects.all()

class CreateRent(CreateAPIView):
    serializer_class = RentedSerializer
    permission_classes = [IsAuthenticated,]

class ReturnRent(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = RentedItem.objects.all()
    serializer_class = ReturnSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'rentedItem_id'
    def perform_update(self, serializer):
        serializer.save(end_datetime=datetime.now())    

class Delete(DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsProductOwner]
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'
