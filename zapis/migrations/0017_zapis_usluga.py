# Generated by Django 2.0.6 on 2019-09-19 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zapis', '0016_sms'),
    ]

    operations = [
        migrations.AddField(
            model_name='zapis',
            name='usluga',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='zapis.Spec'),
            preserve_default=False,
        ),
    ]