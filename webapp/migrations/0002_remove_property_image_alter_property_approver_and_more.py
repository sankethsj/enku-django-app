# Generated by Django 4.2.3 on 2023-07-16 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import webapp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='image',
        ),
        migrations.AlterField(
            model_name='property',
            name='approver',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(webapp.models.get_sentinel_user), related_name='approver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='property',
            name='publisher',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to=settings.AUTH_USER_MODEL),
        ),
    ]
