from django.forms import ModelForm
from django.forms import ValidationError
from datetime import datetime
from django.contrib import messages
from billing_sessions.functions import create_calendars
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
        amount = create_calendars(self.cleaned_data['start'], session)
        session.amount = amount
        session.save()
        self.user.current_session_id = session.id
        self.user.save()

    def clean_start(self):
        start = self.cleaned_data['start']

        now = datetime.now()
        month_diff = (now.year - start.year)*12 + now.month - start.month

        if month_diff >= 12:
            raise ValidationError('Start date must be within 12 months of present date')

        sessions = list(BillingSession.objects.filter(user=self.user))

        if len(sessions) == 0:
            return start
        else:
            most_recent = sessions[-1]
            if most_recent.end is None:
                raise ValidationError('Please end your current session before starting a new one.')
            if start < most_recent.end:
                raise ValidationError("New session must start after the end of last session.")
            return start
