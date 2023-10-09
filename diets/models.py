from django.db import models
from common.models import CommonModel


class SelectedDiet(CommonModel):
    food_name = models.CharField(max_length=250)
    food_calorie = models.FloatField()
    food_gram = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.food_name


class DietList(CommonModel):
    """식단 모델"""

    class MealCategoryChoices(models.TextChoices):
        BREAKFAST = ("breakfast", "아침")
        LUNCH = ("lunch", "점심")
        DINNER = ("dinner", "저녁")
        SNACK = ("snack", "간식")
        NIGHT_SNACK = ("night_snack", "야식")
        DRINK = ("drink", "음료")

    # 식사 종류(아/점/저/간/야/음)
    meal_category = models.CharField(
        max_length=30,
        choices=MealCategoryChoices.choices,
    )
    meal_calorie = models.FloatField()  # 식사당 총 칼로리
    daily_review = models.TextField(
        null=True,
        blank=True,
    )  # 한줄평
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="diets",
    )
    selected_diet = models.ManyToManyField(
        "SelectedDiet",
        through="QuantityMultiple",
        related_name="diets",
    )


class QuantityMultiple(CommonModel):
    diet_list = models.ForeignKey("DietList", on_delete=models.CASCADE)
    selected_diet = models.ForeignKey("SelectedDiet", on_delete=models.CASCADE)
    food_quantity = models.PositiveIntegerField()
