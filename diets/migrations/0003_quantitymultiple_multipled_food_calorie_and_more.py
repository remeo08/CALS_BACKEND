# Generated by Django 4.2.5 on 2023-10-06 11:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diets", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="quantitymultiple",
            name="multipled_food_calorie",
            field=models.FloatField(default=160),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="quantitymultiple",
            name="multipled_food_gram",
            field=models.FloatField(default=300),
            preserve_default=False,
        ),
    ]