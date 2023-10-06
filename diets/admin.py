from django.contrib import admin
from .models import DietList, SelectedDiet


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

# @admin.register(QuantityByDiet)
# class QuantityByDietAdmin(admin.ModelAdmin):
#     list_display = (
#         "created_date",
#         "created_time",
#         "food_info",
#         "food_quantity",
#         "user",
#     )
