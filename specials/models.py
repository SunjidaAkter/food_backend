# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
import math


class Specials(models.Model):
    title = models.CharField(max_length=50, blank=True,null=True)
    description = models.CharField(max_length=500, blank=True,null=True)
    image = models.ImageField(upload_to="specials/images/", blank=True,null=True)
    discount = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

    