from django.db import models
from django.contrib.auth.models import User


class TaskEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=128)
    catigory = models.ChariField(max_length=128)
    complete = models.BooleanField()
