from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import CustomUser

# Create your models here.


class BillingSession(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='sessions')
    start = models.DateField(default=now, unique=True)
    end = models.DateField(null=True, unique=True)
    absentees = models.IntegerField(default=0, validators=[MaxValueValidator(2147483647)])
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['start']
