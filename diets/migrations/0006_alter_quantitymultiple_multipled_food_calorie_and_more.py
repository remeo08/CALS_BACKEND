# Generated by Django 4.2.5 on 2023-10-06 11:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diets", "0005_alter_quantitymultiple_multipled_food_calorie_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quantitymultiple",
            name="multipled_food_calorie",
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="quantitymultiple",
            name="multipled_food_gram",
            field=models.FloatField(default=0, null=True),
        ),
    ]
