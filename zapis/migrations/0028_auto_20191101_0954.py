# Generated by Django 2.0.6 on 2019-11-01 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zapis', '0027_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='sms',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='log',
            name='whatsap',
            field=models.PositiveIntegerField(default=0),
        ),
    ]