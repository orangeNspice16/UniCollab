from django.db import models
from rooms.models import Room

from datetime import datetime
# Create your models here.
class Group(models.Model):
  room = models.ForeignKey(
    'rooms.Room', 
    on_delete=models.CASCADE
  )
  owner = models.ForeignKey(
    'students.Student',
    on_delete=models.CASCADE
  )
  description = models.CharField(max_length=500)
  name = models.CharField(max_length=120)
  preferredmeetingLoc = models.CharField(max_length=500)
  photo = models.ImageField(upload_to='groupAvatar')
  capacity = models.IntegerField(default=5)
  skills = models.CharField(max_length=1000, default="C, Data Modelling, User Interfaces, SQLite, Algorithms")

  def __str__(self):
    return self.name
  
  class Meta:
    unique_together = ['room', 'name']