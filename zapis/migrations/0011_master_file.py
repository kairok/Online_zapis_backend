# Generated by Django 2.0.6 on 2019-09-17 09:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('zapis', '0010_auto_20190912_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='file',
            field=models.FileField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]
