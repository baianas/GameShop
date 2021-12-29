from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from user.forms import RegistrationForm, ChangePasswordForm, ForgotPasswordForm, ForgotPasswordCompleteForm

User = get_user_model()


class RegisterView(View):
    form_class = RegistrationForm
    template_name = 'user/registration.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('register-success'))
        return render(request, self.template_name, {'form': form})


class SuccessfulRegistrationView(TemplateView):
    template_name = 'user/success_registration.html'


class ActivationView(View):
    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return render(request, 'user/activation.html')


class SignInView(LoginView):
    template_name = 'user/login.html'


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'user/change_password.html'
    form_class = ChangePasswordForm

    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm(request=request)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('games'))
        return render(request, self.template_name, {'form': form})


class ForgotPasswordView(View):
    template_name = 'user/forgot_password.html'
    form_class = ForgotPasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.send_mail()
            return redirect(reverse_lazy('forgot-password-complete'))
        return render(request, self.template_name, {'form': form})


class ForgotPasswordCompleteView(View):
    form_class = ForgotPasswordCompleteForm
    template_name = 'user/forgot_password_complete.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('games'))
        return render(request, self.template_name, {'form': form})

