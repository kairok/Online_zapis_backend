# Generated by Django 2.0.6 on 2019-10-11 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zapis', '0020_auto_20190927_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.PositiveIntegerField(default=1)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('adress', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='firma',
            name='smslast',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='firma',
            name='tarif',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='firma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zapis.Firma'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
