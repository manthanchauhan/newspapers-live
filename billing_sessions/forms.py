from django.forms import ModelForm
from django.forms import ValidationError
from django.contrib import messages
from billing_sessions.models import BillingSession


class SessionCreationForm(ModelForm):

    class Meta:
        model = BillingSession
        fields = ('start', )
        labels = {
            'start': 'Start From',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
        kwargs2 = dict()

        for key, value in kwargs.items():
            if key != 'user':
                kwargs2[key] = value

        super(SessionCreationForm, self).__init__(*args, **kwargs2)

    def save(self, commit=True):
        session = super(SessionCreationForm, self).save(commit=False)
        session.user = self.user
        session.save()

    def clean_start(self):
        start = self.cleaned_data['start']
        sessions = list(BillingSession.objects.all())

        if len(sessions) == 0:
            return start
        else:
            most_recent = sessions[-1]
            if most_recent.end is None:
                raise ValidationError("Please end your current session before starting a new one.")
            if start < most_recent.end:
                raise ValidationError("New session must start after the end of last session.")
            return start
