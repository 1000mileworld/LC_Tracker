from django.db import models
from django.urls import reverse
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Problem(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   number = models.IntegerField()
   title = models.CharField(max_length=100)
   #   url = models.CharField(max_length=500)
   #   difficulty = models.CharField(max_length=10)
   #   rating = models.IntegerField(default=1)
   #   categories = models.JSONField()
   #   companies = models.JSONField()
   #   notes = models.TextField()
   #   last_solved = models.DateField()
   #   next_solve = models.DateField()

   def __str__(self):
      return '#'+str(self.number)+' - '+self.title
   
   def get_absolute_url(self):
      return reverse('problems')
   
