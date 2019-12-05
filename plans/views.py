from django.shortcuts import render
from django.views import View
from plans.forms import PlanCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class CreatePlan(View, LoginRequiredMixin):
    template = 'plans/create_plan.html'

    def get(self, request):
        form = PlanCreationForm
        return render(request, self.template, {'form': form})

