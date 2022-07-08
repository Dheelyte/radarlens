# Generated by Django 3.1.4 on 2022-04-17 23:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rating', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0002_auto_20220418_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='businessrating',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.business'),
        ),
        migrations.AddField(
            model_name='businessrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
