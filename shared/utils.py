from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token), 
        }

def linkgenerator(user,len):
    code=get_random_string(len)
    user.otp_code=code
    user.otp_created_at=timezone.now()
    user.save()
    return code

def forgot_pass(user,link):
    subject = 'Password Reset'
    message = f'Hi {user.first_name},\n we have recieved a password change request.\n Please click on the below link to reset your password. \n The validity of the link is 10 minutes. \n {link}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list)
