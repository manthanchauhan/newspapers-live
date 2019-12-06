from django.shortcuts import render, HttpResponse
from django.views import View
from plans.forms import PlanCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class CreatePlan(LoginRequiredMixin, View):
    template = 'plans/create_plan.html'

    def get(self, request):
        form = PlanCreationForm(user=request.user)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = PlanCreationForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return HttpResponse('<h2>Your plan has been saved</h2>')
        else:
            return render(request, self.template, {'form': form})

