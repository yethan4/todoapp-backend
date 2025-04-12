from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers


from .models import CustomUser, Task, List

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'pk',
            'title',
            'due_date',
            'completed',
            'task_list'
        ]
        
class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['name', 'slug']
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password1", "password2")
        extra_kwargs = {"password": {"write_only":True}}
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        
        password = attrs.get("password1", "")
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters!")
        
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")
        
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only = True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials!")

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['email'] = user.email
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        return data