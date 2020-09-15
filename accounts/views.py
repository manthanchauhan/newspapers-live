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
import functions
from django.template.loader import render_to_string


# Create your views here.


def after_login(request):
    if not request.user.is_authenticated:
        return redirect("login")
    try:
        user = CustomUser.objects.get(username=request.user.username)
        var = user.plan
    except ObjectDoesNotExist:
        messages.info(request, "Upload your weekly newspaper plan.")
        return redirect("plans/create_plan")
    return redirect("sessions/home")


class SignUp(View):
    template = "accounts/signup.html"

    def get(self, request, encoded_email, encrypted_hash):
        encrypted_hash = encrypted_hash.replace("slash", "/")
        encoded_email = encoded_email.replace("slash", "/")

        # verify link authenticity
        if not check_data(config("SIGNUP_EMAIL_PHRASE"), encrypted_hash):
            messages.error(request, "Invalid link")
            return redirect("signup")

        email = decode_data(
            config("SIGNUP_EMAIL_ENCODING_SECRET"), encoded_email
        ).decode("utf-8")

        # check if email is already used
        if CustomUser.objects.filter(email=email).exists():
            messages.info(
                request,
                'This email is already in use. Login <a href="'
                + reverse("login")
                + '">here</a>.',
            )
            return redirect("signup")

        form = SignupForm(initial={"email": email})
        return render(request, self.template, {"form": form, "email": email})

    def post(self, request, encoded_email, encrypted_hash):
        encoded_email = encoded_email.replace("slash", "/")
        data = {}

        for key, value in request.POST.items():
            data[key] = value

        # disabled fields are ignored by django forms
        data["email"] = decode_data(
            config("SIGNUP_EMAIL_ENCODING_SECRET"), encoded_email
        ).decode("utf-8")
        form = SignupForm(data)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("after_login")
        else:
            return render(
                request,
                self.template,
                {"form": form, "email": form.cleaned_data.get("email")},
            )


class AboutUs(View):
    template = "accounts/about.html"

    def get(self, request):
        return render(request, self.template)


class EnterEmail(View):
    """
    this view manages the Get Signup Link page: /accounts/signup/
    """

    template = "accounts/enter_email.html"
    email = "accounts/code_email.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        email_id = request.POST["email_id"].strip()

        # check if email already exists
        if CustomUser.objects.filter(email=email_id).count():
            # the user exists
            messages.info(
                request,
                'This email is already in use, login <a href="'
                + reverse("login")
                + '">here</a>.',
            )
            return render(request, self.template)

        pass_phrase = config("SIGNUP_EMAIL_ENCODING_SECRET")
        encoded_email = encode_data(pass_phrase, email_id)
        encoded_email = encoded_email.replace("/", "slash")
        encrypted_hash = encrypt_data(config("SIGNUP_EMAIL_PHRASE"))
        encrypted_hash = encrypted_hash.replace("/", "slash")

        base_url = request.scheme + "://" + request.get_host() + "/accounts/signup/"
        link = base_url + encoded_email + "/" + encrypted_hash + "/"

        message_body = render_to_string(self.email, {"signup_link": link})

        # sending email
        functions.send_mail(
            to_emails=[email_id], content=message_body, subject="Newspapers Invite"
        )

        messages.info(request, "Check your mail for signup link.")
        return redirect("signup")


class PasswordResetEnterEmail(View):
    """
    initiates the forgot password/credentials process
    """

    template = "accounts/forgot_password_enter_email.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        email = request.POST["email_id"].strip()

        # check if user exists
        if not CustomUser.objects.filter(email=email).count():
            messages.error(
                request,
                'User with this email does not exists, signup <a href="'
                + reverse("signup")
                + '">here</a>.',
            )
            return render(request, self.template)

        # get username using email
        user = CustomUser.objects.get(email=email)
        username = user.username

        # create password reset link
        encoded_link = (
            request.scheme
            + "://"
            + request.get_host()
            + "/accounts/password_reset/"
            + encode_data(config("PASSWORD_RESET_PHRASE"), email)
            + "/"
        )

        # send password reset email
        message = render_to_string(
            "accounts/password_reset_email.html",
            {"username": username, "reset_link": encoded_link},
        )
        functions.send_mail(
            to_emails=[email], content=message, subject="Reset Password"
        )

        messages.success(request, "Check your mail for password reset link.")
        return render(request, self.template)


class CreateNewPassword(View):
    """
    creates a new user password
    """

    def get(self, encoded_email):
        # TODO
        pass


def password_reset_done(request):
    """
    called after sending password resend link
    :param request: request
    :return: redirects to same page but with a success message
    """
    messages.success(request, "We've sent you a mail.")
    return redirect("password_reset")
