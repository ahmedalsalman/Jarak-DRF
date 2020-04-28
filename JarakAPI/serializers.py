from rest_framework import serializers
from .models import Product, Profile, RentedItem
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'

    def get_owner(self, obj):
        return "%s" % (obj.owner.username)

class RentedSerializer(serializers.ModelSerializer):
    tenant = serializers.SerializerMethodField()
    product = ProductSerializer()
    
    class Meta:
        model = RentedItem
        fields = '__all__'

    def get_owner(self, obj):
        return "%s" % (obj.tenant.username)

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Profile
		fields = ['location','avatar', 'user']

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
        first_name=validated_data['first_name']
        last_name=validated_data['last_name']
        email=validated_data['email']
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.first_name=(first_name)
        new_user.last_name=(last_name)
        new_user.email=(email)
        new_user.save()
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(allow_blank=True, read_only=True)

    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')

        try:
            user_obj = User.objects.get(username=my_username)
        except:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError(
                "Incorrect username or password!")
        payload = RefreshToken.for_user(user_obj)
        token = str(payload.access_token)

        data["access"] = token
        return data