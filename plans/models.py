from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Plan(models.Model):
    sunday = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    monday = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tuesday = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    wednesday = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    thursday = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    friday = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    saturday = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    billing_date = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)], null=True
    )

    user = models.OneToOneField(
        to=CustomUser, on_delete=models.CASCADE, related_name="plan"
    )

    def to_dict(self):
        return {
            "sunday": self.sunday,
            "monday": self.monday,
            "tuesday": self.tuesday,
            "wednesday": self.wednesday,
            "thursday": self.thursday,
            "friday": self.friday,
            "saturday": self.saturday,
        }
