# Generated by Django 2.0.6 on 2019-09-18 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zapis', '0015_auto_20190918_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newclient', models.BooleanField(default=0)),
                ('beforeday', models.BooleanField(default=0)),
                ('beforehour', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
