from rest_framework import serializers
from .models import Product, Profile, RentedItem
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

# class OwnerSerializer(serializers.ModelSerializer):
#     owner = serializers.SerializerMethodField()
#     owner_id = serializers.SerializerMethodField()
#     class Meta:
#         model=Product
#         fields=['owner_id','owner']

#     def get_owner(self, obj):
#         return obj.user.username

#     def get_owner_id(self, obj):
#         return obj.user.id

class ProductSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    
    class Meta:
        model = Product
        fields = ['id', 'owner', 'name', 'description', 'image', 'image2', 'image3', 'image4']

class RentedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RentedItem
        fields = ['product','end_datetime']



class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','email','username']


class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Profile
		fields = '__all__'


class ProfileUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['location','avatar']        


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

#Authentication-----------------------------------------------------------------------------------------------
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username', 'password']

    def create(self, validated_data):
        new_user = User(**validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return 