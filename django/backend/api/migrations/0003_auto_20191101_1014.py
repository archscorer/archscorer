# Generated by Django 2.2.6 on 2019-11-01 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191031_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=250, verbose_name='username'),
        ),
    ]
