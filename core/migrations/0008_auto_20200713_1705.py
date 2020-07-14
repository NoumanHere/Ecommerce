# Generated by Django 3.0 on 2020-07-13 17:05

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200713_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructions',
            name='Text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='95108', max_length=20),
        ),
    ]
