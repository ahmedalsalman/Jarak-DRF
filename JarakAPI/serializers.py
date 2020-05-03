from rest_framework import serializers
from .models import Product, Profile, RentedItem
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):    
	class Meta:
		model = User
		fields = ['id', 'first_name','last_name','email','username']


class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	avatar = serializers.SerializerMethodField()

	class Meta:
		model = Profile
		fields = ['user', 'location', 'avatar']
	
	def get_avatar(self, obj):
	  return obj.avatar(512)     


class ProductSerializer(serializers.ModelSerializer):
	owner = ProfileSerializer(read_only=True)
	rented_by = serializers.SerializerMethodField()
	# Create ImageSerializer()
	images = ImageSerializer(many=True)
	class Meta:
		model = Product
		fields = ['id', 'owner', 'name', 'description', 'images', 'rented_by']

	def get_rented_by(self, obj):
		return obj.rented_by()


class RentedSerializer(serializers.ModelSerializer):
	class Meta:
		model = RentedItem
		fields = ['tenant', 'product']


class RentedListSerializer(serializers.ModelSerializer):
	product=ProductSerializer()
	tenant=ProfileSerializer()
	class Meta:
		model = RentedItem
		fields = '__all__'


class ProfileUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['location',]


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
		return validated_data