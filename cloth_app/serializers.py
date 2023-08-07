from rest_framework import serializers
from .models import CustomUser,Categories


class CustomUserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """

    class Meta:
        model = CustomUser
        fields = "__all__"

class CategoriesSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """

    class Meta:
        model = Categories
        fields = "__all__"