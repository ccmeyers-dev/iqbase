# Generated by Django 3.0.5 on 2020-06-08 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0019_auto_20200607_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='increase',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=20, null=True),
        ),
    ]
