# Generated by Django 5.0 on 2024-01-23 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0007_remove_train_station_train_from_station_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train',
            name='ticket_price',
        ),
    ]