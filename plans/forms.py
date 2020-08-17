from django.forms import ModelForm
from plans.models import Plan
from django import forms


class PlanCreationForm(ModelForm):
    class Meta:
        model = Plan
        fields = (
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "billing_date",
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("user", None)
        kwargs2 = dict()

        for key, value in kwargs.items():
            if key != "user":
                kwargs2[key] = value

        super(PlanCreationForm, self).__init__(*args, **kwargs2)

    def save(self, commit=True):
        plan = super(PlanCreationForm, self).save(commit=False)
        plan.user = self.user
        plan.save()
