# Generated by Django 4.1.1 on 2023-05-18 13:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0017_alter_usernutrition_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernutrition',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
