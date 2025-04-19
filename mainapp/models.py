from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class StudentData(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    pss_score = models.IntegerField()
    psqi_score = models.IntegerField()
    sleep_hours = models.FloatField()
    activities_hours = models.FloatField()
    prediction_result = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)
