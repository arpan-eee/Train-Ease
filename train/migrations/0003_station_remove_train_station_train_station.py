# Generated by Django 5.0 on 2024-01-18 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0002_delete_trainseat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='train',
            name='station',
        ),
        migrations.AddField(
            model_name='train',
            name='station',
            field=models.ManyToManyField(blank=True, to='train.station'),
        ),
    ]
