from django.forms import ModelForm
from plans.models import Plan


class PlanCreationForm(ModelForm):
    class Meta:
        model = Plan
        fields = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user', None)
        super(PlanCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        plan = super(PlanCreationForm, self).save(commit=False)
        plan.user = self.user
        plan.save()
