# Generated by Django 5.0 on 2024-01-24 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0016_alter_promo_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('text', models.TextField()),
                ('seen', models.BooleanField(default=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
