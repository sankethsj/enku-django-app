# Generated by Django 4.2.3 on 2023-07-16 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_alter_property_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]