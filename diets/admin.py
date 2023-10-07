from django.contrib import admin
from .models import DietList, SelectedDiet, QuantityMultiple


@admin.register(DietList)
class DietListAdmin(admin.ModelAdmin):
    list_display = (
        "created_date",
        "created_time",
        "user",
        "meal_category",
        "meal_calorie",
        "daily_review",
    )

    list_filter = (
        "created_date",
        "meal_category",
    )


@admin.register(SelectedDiet)
class SelectedDietAdmin(admin.ModelAdmin):
    list_display = (
        "created_date",
        "created_time",
        "food_name",
        "food_calorie",
        "food_gram",
    )


@admin.register(QuantityMultiple)
class QuantityMultipleAdmin(admin.ModelAdmin):
    list_display = (
        "diet_list",
        "selected_diet",
        "food_quantity",
        "multipled_food_calorie",
        "multipled_food_gram",
    )
