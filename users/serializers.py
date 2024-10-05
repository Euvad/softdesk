from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {'password': {'write_only': True}} #check standard method to make user serializer

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
