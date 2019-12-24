from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from plans.forms import PlanCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from plans.models import Plan
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class CreatePlan(LoginRequiredMixin, View):
    template = 'plans/create_plan.html'

    def get(self, request):
        try:
            plan = Plan.objects.get(user=request.user)
            form = PlanCreationForm(instance=plan, user=request.user)
        except ObjectDoesNotExist:
            form = PlanCreationForm(user=request.user)
        return render(request, self.template, {'form': form, 'editable': True, 'new': True})

    def post(self, request):
        try:
            Plan.objects.get(user=request.user).delete()
        except ObjectDoesNotExist:
            pass
        form = PlanCreationForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('/sessions/home')
        else:
            return render(request, self.template, {'form': form, 'editable': True, 'new': True})


class EditPlan(LoginRequiredMixin, View):
    template = 'plans/create_plan.html'

    def get(self, request):
        current_session_id = not bool(request.user.current_session_id)
        plan = request.user.plan
        form = PlanCreationForm(instance=plan, user=request.user)
        return render(request, self.template, {'form': form, 'editable': current_session_id, 'new': False})

