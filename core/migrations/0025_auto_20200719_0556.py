# Generated by Django 3.0 on 2020-07-19 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20200719_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='64208', max_length=255),
        ),
    ]
