# Generated by Django 3.0.2 on 2020-06-05 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20200604_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stages', to='api.Series'),
        ),
    ]
