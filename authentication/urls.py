from django.urls import path
from authentication.views import *

urlpatterns=[
    path("register/",RegisterView.as_view()),
    path("login/",LoginView.as_view()),
    path("forgot/password/",ForgotPasswordView.as_view()),
    path("reset/password/<str:code>/",ResetpasswordView.as_view()),
    path("change/password/",ChangePasswordView.as_view()),
    path("forgot/password/otp/",ChangePasswordOTPView.as_view()),
]