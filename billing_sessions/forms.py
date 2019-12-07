from django.forms import ModelForm
from django import forms
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
