from django.contrib.auth import get_user_model

from django import forms

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=6, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password_confirm']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже занят')
        return email

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password2 = data.pop('password_confirm')
        if password != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return data

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(**data)
        user.create_activation_code()
        user.send_activation_mail('register')
        return user


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=6, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_pass = self.cleaned_data.get('old_password')
        user = self.request.user
        if not user.check_password(old_pass):
            raise forms.ValidationError('Укажите верный пароль')
        return old_pass

    def clean(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('password_confirm')
        if pass1 != pass2:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    def save(self):
        new_password = self.cleaned_data.get('password')
        user = self.request.user
        user.set_password(new_password)
        user.save()


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь не найден')
        return email

    def send_mail(self):
        email = self.cleaned_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.send_activation_mail('forgot_password')


class ForgotPasswordCompleteForm(forms.Form):
    code = forms.CharField(min_length=8, max_length=8)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=6, widget=forms.PasswordInput)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not User.objects.filter(activation_code=code).exists():
            raise forms.ValidationError('Неверный код подтверждения')
        return code

    def clean(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('password_confirm')
        if pass1 != pass2:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    def save(self):
        code = self.cleaned_data.get('code')
        password = self.cleaned_data.get('password')
        user = User.objects.get(activation_code=code)
        user.set_password(password)
        user.save()
