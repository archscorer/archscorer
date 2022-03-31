# Generated by Django 4.0.2 on 2022-03-14 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_alter_participant_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unisex')], default='U', max_length=1, verbose_name='gender'),
        ),
    ]