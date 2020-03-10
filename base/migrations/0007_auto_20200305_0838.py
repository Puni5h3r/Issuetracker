# Generated by Django 3.0.3 on 2020-03-05 08:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20200223_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='weight',
            field=models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]