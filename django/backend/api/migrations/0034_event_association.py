# Generated by Django 4.0.2 on 2022-03-16 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_alter_levelclass_age_group_alter_levelclass_style_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='association',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='api.association'),
        ),
    ]
