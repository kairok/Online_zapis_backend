# Generated by Django 2.0.6 on 2019-08-15 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=100)),
                ('profession', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Workcalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.CharField(max_length=5)),
                ('end', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Zapis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.CharField(max_length=5)),
                ('end', models.CharField(max_length=5)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zapis.Client')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zapis.Master')),
            ],
        ),
    ]
