from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from billing_sessions.models import BillingSession

# Create your models here.


class Calendar(models.Model):
    session = models.ForeignKey(
        to=BillingSession, on_delete=models.CASCADE, related_name="calendars"
    )
    start = models.DateField(default=now)
    end = models.DateField(null=True)
    absentees = models.IntegerField(
        default=0, validators=[MaxValueValidator(2147483647)]
    )
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["start"]
