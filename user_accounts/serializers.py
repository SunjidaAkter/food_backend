from rest_framework import serializers
from . import models
from .models import UserAccounts
from django.contrib.auth.models import User
class UserAccountsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.UserAccounts
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    mobile_no = serializers.CharField(required=False, allow_blank=True)
    image = serializers.URLField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'mobile_no', 'image', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': "Passwords do not match"})
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({'email': "Email already exists"})
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        
        # Create or update UserAccounts
        UserAccounts.objects.create(
            user=user,
            mobile_no=validated_data.get('mobile_no', ''),
            image=validated_data.get('image', ''),
            address=validated_data.get('address', '')
        )
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)