# Generated by Django 3.0 on 2020-07-19 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20200719_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='86238', max_length=255),
        ),
    ]
