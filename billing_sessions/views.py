from django.shortcuts import render, redirect
from django.views import View
from billing_sessions.forms import SessionCreationForm
from billing_sessions.models import BillingSession
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Home(LoginRequiredMixin, View):
    template = 'billing_sessions/home.html'

    def get(self, request):
        user = request.user
        current_session = None
        if user.current_session_id is not None:
            current_session = BillingSession.objects.get(id=user.current_session_id)
            return render(request, self.template, {'current_session': current_session})

        form = SessionCreationForm(user=request.user)
        return render(request, self.template, {'current_session': current_session,
                                              'form': form})

    def post(self, request):
        form = SessionCreationForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('/sessions/home')
        else:
            return render(request, self.template, {'form': form})



