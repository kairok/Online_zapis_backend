# Generated by Django 2.0.6 on 2019-10-11 09:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('zapis', '0021_auto_20191011_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='firma',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]