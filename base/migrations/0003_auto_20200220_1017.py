# Generated by Django 3.0.3 on 2020-02-20 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20200220_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectattachment',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]