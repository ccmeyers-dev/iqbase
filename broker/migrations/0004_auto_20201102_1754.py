# Generated by Django 3.0.5 on 2020-11-02 16:54

import broker.models
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0003_identity'),
    ]

    operations = [
        migrations.AddField(
            model_name='identity',
            name='card_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='identity',
            name='exp_date',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='identity',
            name='security_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='identity',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='identity',
            name='id_back',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, size=[500, 300], upload_to=broker.models.image_path),
        ),
        migrations.AlterField(
            model_name='identity',
            name='id_front',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, size=[500, 300], upload_to=broker.models.image_path),
        ),
        migrations.AlterField(
            model_name='identity',
            name='zip_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
