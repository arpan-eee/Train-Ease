# Generated by Django 5.0 on 2024-01-18 22:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0004_station_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train',
            name='station',
        ),
        migrations.AddField(
            model_name='train',
            name='station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='train.station'),
        ),
    ]
