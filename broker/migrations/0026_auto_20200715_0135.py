# Generated by Django 3.0.5 on 2020-07-15 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0025_trade_deposit_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='deposit_date',
        ),
        migrations.AlterField(
            model_name='trade',
            name='withdrawal_date',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
