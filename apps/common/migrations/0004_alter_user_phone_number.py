# Generated by Django 4.0.4 on 2023-06-16 11:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_alter_user_options_rename_name_user_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=12, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must start from 998 and contain 9 characters. For example: 998998065999', regex='^998\\d{9}$')]),
        ),
    ]