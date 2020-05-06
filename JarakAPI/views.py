from django.contrib.auth.models import User
from django.shortcuts import render

from .models import Product, Profile, RentedItem
from .permissions import IsProductOwner, ProfileOwner
from .serializers import  (
    ProductSerializer, RentedListSerializer, ProfileSerializer,
    ProfileUpdateSerializer, CreateProductSerializer, UserCreateSerializer,
    RentedSerializer, ReturnSerializer
)

from rest_framework.generics import (
    ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView,
    DestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from datetime import datetime



class Register(CreateAPIView):
    serializer_class = UserCreateSerializer


class ProductList(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class Profile(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ProfileOwner]
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        if profile_id is None:
            return Profile.objects.get(user=self.request.user)
        else:
            return Profile.objects.get(id=profile_id)


class ProductUpdate(UpdateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)


class RentList(ListAPIView):
    serializer_class = RentedListSerializer
    queryset = RentedItem.objects.all()


class Rent(CreateAPIView):
    serializer_class = RentedSerializer
    permission_classes = [IsAuthenticated,]


class ReturnRent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, rented_item_id, *args, **kwargs):
        obj = RentedItem.objects.get(id=rented_item_id)
        obj.end_datetime = datetime.now()
        obj.save()
        return Response({"msg": "yay"})


class ProductDelete(DestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'
    permission_classes = [IsAuthenticated, IsProductOwner]
