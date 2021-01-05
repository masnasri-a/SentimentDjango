from django.db import models
from django import forms

class PostModel(models.Model):
    fullname    = models.CharField(max_length=20)
    username    = models.CharField(max_length=20)
    email       = models.EmailField()
    phones      = models.CharField(max_length=20)
    password    = models.CharField(max_length=20)

class input_sentimen(models.Model):
    input = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.input