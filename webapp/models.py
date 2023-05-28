from django.db import models

# Create your models here.

class Card(models.Model):
    username = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    pub_date = models.DateTimeField("published date")
    update_date = models.DateTimeField("updated date")
