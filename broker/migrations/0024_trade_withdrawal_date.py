# Generated by Django 3.0.5 on 2020-07-14 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0023_auto_20200715_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='withdrawal_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
