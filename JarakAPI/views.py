from django.contrib.auth.models import User
from django.shortcuts import render

from .models import Product, Profile, RentedItem
from .permissions import IsProductOwner
from .serializers import  (
    ProductSerializer, RentedListSerializer, ProfileSerializer, 
    ProfileUpdateSerializer, CreateProductSerializer, 
    UserCreateSerializer, RentedSerializer, ReturnSerializer
)
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView, CreateAPIView, UpdateAPIView,
     RetrieveAPIView, DestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from datetime import datetime

class ProductList(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)


class ProductUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'


class ProductDelete(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsProductOwner]
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'


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
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'profile_id'
    #Not used yet, but it will be to used to update the profile image for the user instead of the default generated one.
    def perform_update(self, serializer):
        avatar=Profile.objects.all()
        serializer.save(image=avatar.image)  


class RentList(ListAPIView):
    serializer_class = RentedListSerializer
    queryset = RentedItem.objects.all()


class Rent(CreateAPIView):
    serializer_class = RentedSerializer
    permission_classes = [IsAuthenticated]


class ReturnRental(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, rented_item_id, *args, **kwargs):
        obj = RentedItem.objects.get(id=rented_item_id)
        obj.end_datetime = datetime.now()
        obj.save()
        return Response({"msg": "Item Returned Successfully"})

        
class Register(CreateAPIView):
    serializer_class = UserCreateSerializer
