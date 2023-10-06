from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User
from math import floor
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "password",
        )


class RecommendedCalorieMixin:
    def get_recommended_calorie(self, user):
        age = int(user.age)
        height = int(user.height)
        weight = int(user.weight)
        gender = user.gender
        activity = user.activity

        activity_coefficients = {
            "lowest": 1.0,
            "low": 1.11,
            "middle": 1.25,
            "high": 1.48,
            "female_lowest": 1.0,
            "female_low": 1.12,
            "female_middle": 1.27,
            "female_high": 1.45,
        }

        if gender == "male":
            recommended_calorie = floor(
                activity_coefficients.get(activity, 1.0)
                * ((6.25 * height) + (10 * weight) - (5 * age) + 5)
            )
        elif gender == "female":
            recommended_calorie = floor(
                activity_coefficients.get(f"female_{activity}", 1.0)
                * ((6.25 * height) + (10 * weight) - (5 * age) - 161)
            )
        return recommended_calorie


class UserSerializer(ModelSerializer, RecommendedCalorieMixin):
    recommended_calorie = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "is_active",
            "email",
            "age",
            "gender",
            "height",
            "weight",
            "activity",
            "recommended_calorie",
        )


class UserPutSerializer(ModelSerializer, RecommendedCalorieMixin):
    recommended_calorie = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "height",
            "weight",
            "activity",
            "recommended_calorie",
        )
