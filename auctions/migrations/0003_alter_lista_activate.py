# Generated by Django 5.1.1 on 2024-09-19 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_lista_activate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista',
            name='activate',
            field=models.BooleanField(default=True),
        ),
    ]
