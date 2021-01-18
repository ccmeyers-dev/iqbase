# Generated by Django 3.0.5 on 2021-01-17 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0007_auto_20210117_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='withdrawal_date',
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='broker.Customer')),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='broker.Wallet')),
            ],
        ),
    ]
