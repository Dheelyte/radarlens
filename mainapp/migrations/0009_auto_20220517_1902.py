# Generated by Django 3.1.4 on 2022-05-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_business_show_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='show_location',
            field=models.BooleanField(default=False),
        ),
    ]
