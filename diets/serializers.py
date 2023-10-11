from rest_framework.serializers import ModelSerializer, SerializerMethodField
from math import floor
from django.db.models import Sum
from .models import DietList, SelectedDiet, QuantityMultiple
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


class QuantityMultipleSerializer(serializers.ModelSerializer):
    selected_diet = serializers.SelectedDietSerializer()

    class Meta:
        model = QuantityMultiple
        fields = (
            "food_quantity",
            "selected_diet",
        )


class DietSerializer(serializers.ModelSerializer, RecommendedCalorieMixin):
    daily_star_rating = serializers.SerializerMethodField()
    daily_calorie_sum = serializers.SerializerMethodField()
    selected_diet_quantity = serializers.QuantityMultipleSerializer(
        source="quantitymultiple_set",
        read_only=True,
        many=True,
    )

    class Meta:
        model = DietList
        fields = (
            "meal_category",
            "meal_calorie",
            "daily_review",
            "selected_diet_quantity",
            "created_date",
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

        meal_calorie = float(meal_calorie)

        total_calorie = daily_total_calorie + meal_calorie

        if 0 <= total_calorie and total_calorie <= recommended_calorie:
            return 5.0
        elif recommended_calorie < total_calorie:
            calorie_difference = total_calorie - recommended_calorie
            if calorie_difference <= 100:
                star = 4.0
            elif calorie_difference <= 200:
                star = 3.0
            elif calorie_difference <= 300:
                star = 2.0
            elif calorie_difference <= 400:
                star = 1.0
            else:
                star = 0.0
            return star


class ReviewPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietList
        fields = (
            "daily_review",
            "created_date",
        )
