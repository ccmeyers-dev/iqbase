# Generated by Django 3.0.5 on 2020-07-17 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='code',
            field=models.CharField(default='BTC', max_length=8),
        ),
    ]
