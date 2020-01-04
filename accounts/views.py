from django.shortcuts import render, redirect, reverse
from django.views import View
from accounts.forms import SignupForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from accounts.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from .functions import encode_data, encrypt_data, check_data, decode_data
from decouple import config
from django.utils.html import format_html
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.


def after_login(request):
    try:
        user = CustomUser.objects.get(username=request.user.username)
        var = user.plan
    except ObjectDoesNotExist:
        messages.info(request, 'Upload your weekly newspaper plan.')
        return redirect('plans/create_plan')
    return redirect('sessions/home')


class SignUp(View):
    template = 'accounts/signup.html'

    def get(self, request, encoded_email, encrypted_hash):
        encrypted_hash = encrypted_hash.replace('slash', '/')
        encoded_email = encoded_email.replace('slash', '/')

        # verify link authenticity
        if not check_data(config('SIGNUP_EMAIL_PHRASE'), encrypted_hash):
            messages.error(request, 'Invalid link')
            return redirect('signup')

        email = decode_data(config('SIGNUP_EMAIL_ENCODING_SECRET'), encoded_email).decode('utf-8')

        # check if email is already used
        if CustomUser.objects.filter(email=email).exists():
            messages.info(request, 'This email is already in use. Login <a href="' + reverse('login') + '">here</a>.')
            return redirect('signup')

        form = SignupForm(initial={'email': email})
        return render(request, self.template, {'form': form, 'email': email})

    def post(self, request, encoded_email, encrypted_hash):
        encoded_email = encoded_email.replace('slash', '/')
        data = {}

        for key, value in request.POST.items():
            data[key] = value

        # disabled fields are ignored by django forms
        data['email'] = decode_data(config('SIGNUP_EMAIL_ENCODING_SECRET'), encoded_email).decode('utf-8')
        form = SignupForm(data)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('after_login')
        else:
            return render(request, self.template, {'form': form, 'email': form.cleaned_data.get('email')})


class AboutUs(View):
    template = 'accounts/about.html'

    def get(self, request):
        return render(request, self.template)


class EnterEmail(View):
    template = 'accounts/enter_email.html'
    email = 'accounts/code_email.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        email_id = request.POST['email_id'].strip()
        pass_phrase = config('SIGNUP_EMAIL_ENCODING_SECRET')
        encoded_email = encode_data(pass_phrase, email_id)
        encoded_email = encoded_email.replace('/', 'slash')
        encrypted_hash = encrypt_data(config('SIGNUP_EMAIL_PHRASE'))
        encrypted_hash = encrypted_hash.replace('/', 'slash')

        base_url = request.scheme + '://' + request.get_host() + '/accounts/signup/'
        link = base_url + encoded_email + '/' + encrypted_hash + '/'

        message_body = render_to_string(self.email, {'signup_link': link})
        send_mail(subject='Newspapers signup link', message=message_body,
                  from_email=settings.EMAIL_HOST_USER, recipient_list=[email_id])

        messages.info(request, 'Check your mail for signup link.')
        return redirect('signup')


