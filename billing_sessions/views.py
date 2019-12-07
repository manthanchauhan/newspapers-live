from django.shortcuts import render
from django.views import View
from billing_sessions.forms import SessionCreationForm
from billing_sessions.models import BillingSession
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Home(LoginRequiredMixin, View):
    tempate = 'billing_sessions/home.html'

    def get(self, request):
        user = request.user
        current_session = None
        if user.current_session_id is not None:
            current_session = BillingSession.objects.get(id=user.current_session_id)
            return render(request, self.tempate, {'current_session': current_session})

        form = SessionCreationForm(user=request.user)
        return render(request, self.tempate, {'current_session': current_session,
                                              'form': form})

