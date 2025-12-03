# users/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, UserType


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone', 'birth_date', 'user_type', 'image']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Nested serializer
    token = serializers.SerializerMethodField(read_only=True)  # token alanı

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.update_or_create(user=user, defaults=profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()

        if profile_data:
            profile = instance.profile
            profile.phone = profile_data.get('phone', profile.phone)
            profile.birth_date = profile_data.get('birth_date', profile.birth_date)
            profile.user_type = profile_data.get('user_type', profile.user_type)
            if 'image' in profile_data:
                profile.image = profile_data['image']
            profile.save()
    
    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class UserTypeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()  # alt tipleri göstermek için

    class Meta:
        model = UserType
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        # Eğer alt tip varsa recursive olarak göster
        if obj.children.exists():
            return UserTypeSerializer(obj.children.all(), many=True).data
        return []


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    # username = serializers.SerializerMethodField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Email ile kullanıcıyı bul
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email veya şifre hatalı.")

        # Password kontrol
        if not user.check_password(password):
            raise serializers.ValidationError("Email veya şifre hatalı.")

        # Username'i SimpleJWT'ye ver (JWT username üzerinden çalışır)
        attrs['username'] = user.username

        return super().validate(attrs)
    
    # def get_username(self, instance):
    #     user = User.objects.get(email=instance.email)
    #     return user.username