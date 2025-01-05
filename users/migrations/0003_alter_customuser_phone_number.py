# Generated by Django 5.1.4 on 2025-01-05 08:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^(\\+254|0)([7][0-9]|[1][0-1]){1}[0-9]{1}[0-9]{6}$')]),
        ),
    ]
