# Generated by Django 3.2.2 on 2021-05-13 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20201009_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='levelclass',
            name='age_group',
            field=models.CharField(choices=[('T', 'Tidet'), ('C', 'Cub'), ('CA', 'Cadet'), ('J', 'Junior'), ('YA', 'Young Adult'), ('A', 'Adult'), ('V', 'Veteran')], max_length=2, verbose_name='age group'),
        ),
        migrations.AlterField(
            model_name='levelclass',
            name='style',
            field=models.CharField(choices=[('BB-C', 'Barebow Compound'), ('BB-R', 'Barebow Recurve'), ('BH-C', 'Bowhunter Compound'), ('BH-R', 'Bowhunter Recurve'), ('BL', 'Bowhunter Limited'), ('BU', 'Bowhunter Unlimited'), ('FS-C', 'Freestyle Limited Compound'), ('FS-R', 'Freestyle Limited Recurve'), ('FU', 'Freestyle Unlimited'), ('HB', 'Historic Longbow'), ('LB', 'Longbow'), ('TR', 'Traditional Recurve'), ('**', 'Variable'), ('R', 'Recurve'), ('C', 'Compound'), ('I', 'Instinctive'), ('L', 'Longbow')], max_length=5, verbose_name='Shooting style'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='age_group',
            field=models.CharField(choices=[('T', 'Tidet'), ('C', 'Cub'), ('CA', 'Cadet'), ('J', 'Junior'), ('YA', 'Young Adult'), ('A', 'Adult'), ('V', 'Veteran')], max_length=2, verbose_name='age group'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='style',
            field=models.CharField(choices=[('BB-C', 'Barebow Compound'), ('BB-R', 'Barebow Recurve'), ('BH-C', 'Bowhunter Compound'), ('BH-R', 'Bowhunter Recurve'), ('BL', 'Bowhunter Limited'), ('BU', 'Bowhunter Unlimited'), ('FS-C', 'Freestyle Limited Compound'), ('FS-R', 'Freestyle Limited Recurve'), ('FU', 'Freestyle Unlimited'), ('HB', 'Historic Longbow'), ('LB', 'Longbow'), ('TR', 'Traditional Recurve'), ('**', 'Variable'), ('R', 'Recurve'), ('C', 'Compound'), ('I', 'Instinctive'), ('L', 'Longbow')], max_length=5, verbose_name='Shooting style'),
        ),
        migrations.AlterField(
            model_name='record',
            name='age_group',
            field=models.CharField(choices=[('T', 'Tidet'), ('C', 'Cub'), ('CA', 'Cadet'), ('J', 'Junior'), ('YA', 'Young Adult'), ('A', 'Adult'), ('V', 'Veteran')], max_length=2, verbose_name='age group'),
        ),
        migrations.AlterField(
            model_name='record',
            name='style',
            field=models.CharField(choices=[('BB-C', 'Barebow Compound'), ('BB-R', 'Barebow Recurve'), ('BH-C', 'Bowhunter Compound'), ('BH-R', 'Bowhunter Recurve'), ('BL', 'Bowhunter Limited'), ('BU', 'Bowhunter Unlimited'), ('FS-C', 'Freestyle Limited Compound'), ('FS-R', 'Freestyle Limited Recurve'), ('FU', 'Freestyle Unlimited'), ('HB', 'Historic Longbow'), ('LB', 'Longbow'), ('TR', 'Traditional Recurve'), ('**', 'Variable'), ('R', 'Recurve'), ('C', 'Compound'), ('I', 'Instinctive'), ('L', 'Longbow')], max_length=5, verbose_name='Shooting style'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
