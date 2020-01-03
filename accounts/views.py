from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from accounts.forms import SignupForm
from django.contrib.auth import authenticate, login
from accounts.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def after_login(request):
    try:
        user = CustomUser.objects.get(username=request.user.username)
        var = user.plan
    except ObjectDoesNotExist:
        return redirect('plans/create_plan')
    return redirect('sessions/home')


class SignUp(View):
    template = 'accounts/signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            print(user)
            login(request, user)
            return redirect('after_login')
        else:
            return render(request, self.template, {'form': form})


class AboutUs(View):
    template = 'accounts/about.html'

    def get(self, request):
        return render(request, self.template)
