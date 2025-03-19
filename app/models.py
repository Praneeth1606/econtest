from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User, AbstractUser, Group, Permission


class Participant(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="participant_set",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="participant_set",
        blank=True
    )
    contact = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    rem_time = models.IntegerField(default=0)
    
class Result(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="result")
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

class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="submission")
    qnno = models.IntegerField()
    mark = models.IntegerField()
    message = models.TextField()
    timeofs = models.CharField(max_length=100)
 