# Generated by Django 3.1.4 on 2022-08-02 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_delete_websitevisit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='show_location',
            field=models.BooleanField(default=True),
        ),
    ]
