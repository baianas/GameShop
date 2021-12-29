from django.contrib.auth.views import LogoutView
from django.urls import path

from user.views import (RegisterView, SuccessfulRegistrationView, ActivationView, SignInView,
                        ChangePasswordView, ForgotPasswordView, ForgotPasswordCompleteView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/success/',
         SuccessfulRegistrationView.as_view(),
         name='register-success'),
    path('activate/<str:code>/', ActivationView.as_view(), name='activate'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('forgot_password/complete', ForgotPasswordCompleteView.as_view(), name='forgot-password-complete')
]
