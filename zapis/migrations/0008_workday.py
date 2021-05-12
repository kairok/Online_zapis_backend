# Generated by Django 2.0.6 on 2019-09-03 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zapis', '0007_auto_20190828_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomday', models.IntegerField()),
                ('nameday', models.CharField(max_length=10)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zapis.Master')),
            ],
        ),
    ]