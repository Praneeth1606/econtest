from django.db import models
from datetime import datetime, timedelta
# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)    # set this to unique
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    done = models.BooleanField(default=False)
    rem_time = models.IntegerField(default=0)
    
class Result(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="result")
    q1s = models.IntegerField(default=0)
    q2s = models.IntegerField(default=0)
    q3s = models.IntegerField(default=0)
    q4s = models.IntegerField(default=0)
    q5s = models.IntegerField(default=0)
    q6s = models.IntegerField(default=0)
    q7s = models.IntegerField(default=0)
    q8s = models.IntegerField(default=0)
    q1t = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000)
    q2t = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000)
    q3t = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000)
    q4t = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000)
    q5t = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000)
    q6t = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000)
    q7t = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000)
    q8t = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000)
    tot_score = models.IntegerField(default=0)
    tot_time = models.DecimalField(max_digits=14, decimal_places=4, default=0.0000)
    # date = models.DateTimeField(auto_now_add=True)

class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submission")
    qnno = models.IntegerField()
    mark = models.IntegerField()
    message = models.TextField()
    timeofs = models.CharField(max_length=100)
 