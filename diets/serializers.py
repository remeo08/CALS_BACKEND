from rest_framework.serializers import ModelSerializer, SerializerMethodField
from math import floor
from django.db.models import Sum
from .models import DietList, SelectedDiet
from . import serializers
from users.serializers import RecommendedCalorieMixin


class SelectedDietSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedDiet
        fields = (
            "food_name",
            "food_calorie",
            "food_gram",
        )


class DietSerializer(serializers.ModelSerializer, RecommendedCalorieMixin):
    daily_star_rating = serializers.SerializerMethodField()
    daily_calorie_sum = serializers.SerializerMethodField()
    selected_diet = serializers.SelectedDietSerializer(read_only=True , many=True)

    class Meta:
        model = DietList
        fields = (
            "meal_category",
            "meal_calorie", 
            "daily_review",
            "selected_diet",
            "created_date",
            "created_time",
            "updated_at",
            "daily_star_rating",
            "daily_calorie_sum",
        )

    def get_daily_calorie_sum(self, diets):
        total_rating = DietList.objects.filter(
            created_date=diets.created_date, user=diets.user
        ).aggregate(Sum("meal_calorie"))
        daily_calorie = total_rating["meal_calorie__sum"]
        if daily_calorie is None:
            daily_calorie = 0
        return daily_calorie

    def get_daily_star_rating(self, diets):
        daily_total_calorie = self.get_daily_calorie_sum(diets)
        meal_calorie = diets.meal_calorie
        recommended_calorie = self.get_recommended_calorie(diets.user)

        total_calorie = daily_total_calorie + meal_calorie

        if total_calorie <= recommended_calorie:
            return 5.0

        calorie_difference = total_calorie - recommended_calorie
        rating = 5.0 - floor(calorie_difference / 100) * 0.5
        return max(0.0, rating)
