from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Problem(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
     number = models.IntegerField()
     title = models.CharField(max_length=100)
     url = models.CharField(max_length=500)
     difficulty = models.CharField(max_length=10)
     rating = models.IntegerField()
     categories = models.JSONField()
     companies = models.JSONField()
     notes = models.TextField()
     last_solved = models.DateField()
     next_solve = models.DateField()

     def __str__(self):
        return '#'+str(self.number)+' - '+self.title
