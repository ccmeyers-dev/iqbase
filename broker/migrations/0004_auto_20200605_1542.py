# Generated by Django 3.0.6 on 2020-06-05 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0003_wallet_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='id_back',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='customer',
            name='id_front',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
