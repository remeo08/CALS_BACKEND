# Generated by Django 4.2.5 on 2023-10-09 05:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("diets", "0006_alter_quantitymultiple_multipled_food_calorie_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quantitymultiple",
            name="multipled_food_calorie",
        ),
        migrations.RemoveField(
            model_name="quantitymultiple",
            name="multipled_food_gram",
        ),
    ]
