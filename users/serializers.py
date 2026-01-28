from .enums import UserRole
from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match")

        password = attrs.get('password1')
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if attrs.get('role') not in UserRole.values:
            raise serializers.ValidationError(f"Role must be {UserRole.EMPLOYEE} or {UserRole.RESTAURANT}")

        if attrs.get('role') == UserRole.ADMIN:
            raise serializers.ValidationError("Role cannot register as an Admin via this endpoint")

        return attrs


    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        return User.objects.create_user(password=password, **validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if not user:
                raise serializers.ValidationError("Incorrect email or password")

            if not user.is_active:
                raise serializers.ValidationError("This account is inactive")

            return user

        raise serializers.ValidationError("Both email and password are required")


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
