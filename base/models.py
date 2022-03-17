from django.db import models
from django.urls import reverse
from django.conf import settings
User = settings.AUTH_USER_MODEL

#from django.core.validators import MinValueValidator
#from django.contrib.postgres.fields import ArrayField #only for Postgres
from datetime import datetime as dt
DIFFICULTY_CHOICES = (
    ('Easy','Easy'),
    ('Medium', 'Medium'),
    ('Hard','Hard'),
)

RATING_CHOICES = (
   ('1','1 (Solved optimally as fast as I can type)'),
   ('2','2 (Solved in <30 min with few bugs)'),
   ('3','3 (Solved in 1 hr with some bugs)'),
   ('4',"4 (Couldn't solve myself, but understood solution)"),
   ('5',"5 (If interviewer asks this, I'm doomed)"),
)

class Problem(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   number = models.PositiveIntegerField()
   title = models.CharField(max_length=100)
   link = models.URLField(max_length=500, default="")
   difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, default='medium')
   rating = models.CharField(verbose_name='Self Difficulty Rating', max_length=2, choices=RATING_CHOICES, default='3')
   # #categories = ArrayField(models.CharField(max_length=50, blank=True), default=list) #blank=True to make field optional
   categories = models.TextField(default='', verbose_name="Category Tags (comma separated)", blank=True)
   companies = models.TextField(default='', verbose_name="Company Tags (comma separated)", blank=True)
   notes = models.TextField(default='', blank=True)
   last_solved = models.DateField(default=dt.now().date())
   next_solve = models.DateField(null=True, blank=True)

   def __str__(self):
      return '#'+str(self.number)+' - '+self.title
   
   def get_absolute_url(self):
      return reverse('problems')
   
