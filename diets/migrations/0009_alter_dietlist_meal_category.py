# Generated by Django 4.2.5 on 2023-10-11 02:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diets", "0008_remove_dietlist_created_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dietlist",
            name="meal_category",
            field=models.CharField(
                choices=[
                    ("breakfast", "아침"),
                    ("lunch", "점심"),
                    ("dinner", "저녁"),
                    ("snack", "간식"),
                ],
                max_length=30,
            ),
        ),
    ]
