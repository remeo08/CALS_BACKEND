# Generated by Django 4.2.5 on 2023-10-06 04:23

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SelectedDiet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateField(auto_now_add=True)),
                ("created_time", models.TimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("food_name", models.CharField(max_length=250)),
                ("food_calorie", models.FloatField()),
                ("food_gram", models.PositiveIntegerField()),
                ("food_quantity", models.PositiveIntegerField(default=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DietList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateField(auto_now_add=True)),
                ("created_time", models.TimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "meal_category",
                    models.CharField(
                        choices=[
                            ("breakfast", "아침"),
                            ("lunch", "점심"),
                            ("dinner", "저녁"),
                            ("snack", "간식"),
                            ("night_snack", "야식"),
                            ("drink", "음료"),
                        ],
                        max_length=30,
                    ),
                ),
                ("meal_calorie", models.FloatField()),
                ("daily_review", models.TextField(blank=True, null=True)),
                (
                    "selected_diet",
                    models.ManyToManyField(
                        related_name="diets", to="diets.selecteddiet"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]