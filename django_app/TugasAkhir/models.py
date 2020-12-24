from django.db import models

class PostModel(models.Model):
    fullname    = models.CharField(max_length=20)
    username    = models.CharField(max_length=20)
    email       = models.EmailField()
    phones      = models.CharField(max_length=20)
    password    = models.CharField(max_length=20)