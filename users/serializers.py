import string
from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError("Passwords must match.")
        # Password policy
        password = data['password']

        errors = []

        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
            errors.append("Password must contain at least one letter.")
        if not any(char.isupper() for char in password):
            errors.append("Password must contain at least one uppercase letter.")
        if not any(char in string.punctuation for char in password):
            errors.append("Password must contain at least one special character.")

        # check is errors not empty and trow validation exception
        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        validated_data.pop('repeat_password')  # Remove repeat_password from validated_data
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'repeat_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'repeat_password': {'write_only': True},
        }

