from django.shortcuts import render
from django.views import View
from billing_sessions.models import BillingSession
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Home(LoginRequiredMixin, View):
    tempate = 'billing_sessions/home.html'

    def get(self, request):
        user = request.user
        billing_sessions = list(BillingSession.objects.all().filter(user=user))
        return render(request, self.tempate, {'billing_sessions': billing_sessions})
