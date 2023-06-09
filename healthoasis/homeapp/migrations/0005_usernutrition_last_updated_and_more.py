# Generated by Django 4.1.1 on 2023-05-17 13:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0004_remove_usernutrition_name_alter_usernutrition_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernutrition',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='usernutrition',
            name='calories',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
