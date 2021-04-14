from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from .permissions import ValidateApiKey
from authentication.serializer import *
from shared.utils import *
# Create your views here.


class RegisterView(APIView):
    permission_classes = (ValidateApiKey,)
    def post(self,request):
        output_status=False
        output_detail="Failed"
        res_status=status.HTTP_400_BAD_REQUEST
        data=[]
        serializer=CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            output_status=True
            output_detail="Success"
            res_status=status.HTTP_200_OK
            data=serializer.data
        else:
            data=serializer.errors
        context={
            "status":output_status,
            "detail":output_detail,
            "data":data
        }
        return Response(context,status=res_status)

class LoginView(APIView):
    permission_classes = (ValidateApiKey,)
    def post(self,request):
        output_status=False
        output_detail="Failed"
        res_status=status.HTTP_400_BAD_REQUEST
        data=[]
        email=request.data.get("email")
        password=request.data.get("password")
        if email:
            model=User.objects.filter(email=email).first()
            if model:
                check_password=model.check_password(password)
                if check_password:
                    output_status=True
                    output_detail="Success"
                    res_status=status.HTTP_200_OK
                    data.append(get_token(model))
                else:
                    output_detail="Wrong password"
            else:
                output_detail="Wrong email"
        else:
            output_detail="Please provide email"
        context={
            "status":output_status,
            "detail":output_detail,
            "data":data
        }
        return Response(context,status=res_status)

class ForgotPasswordView(APIView):
    def post(self,request):
        user=request.user
        output_status=False
        output_detail="Falied"
        res_status=status.HTTP_400_BAD_REQUEST
        user_email=request.data.get("email",None)
        if user.email == user_email :
            code=linkgenerator(user,10)
            host = request.get_host()
            if request.is_secure():
                protocol = 'https://'
            else:
                protocol = 'http://'  
            link=protocol + host +  "api/auth/reset/password/" + code + "/"
            forgot_pass(user,link)   
            output_status=True
            output_detail="Opt send to your verified email"
            res_status=status.HTTP_200_OK
        else:
            output_detail="Wrong email"
        context={
            "status":output_status,
            "detail":output_detail
        }    
        return Response(context,status=res_status)

class ResetpasswordView(APIView):
    def post(self,request,code):
        user=request.user
        output_status=False
        output_detail="Falied"
        res_status=status.HTTP_400_BAD_REQUEST
        if user.otp_code == code :
            time=timezone.now()-user.otp_created_at
            if time.seconds < 600 :
                password=request.data.get("password",None)
                if password:
                    user.set_password(password)
                    user.otp_code=""
                    user.save()
                    output_status=True
                    output_detail="New password saved"
                    res_status=status.HTTP_200_OK
                else:
                    output_detail="Please enter password"
            else:
                output_detail="Timeout , Please generate new OTP"
        else:
            output_detail="OTP does not match"
        context={
            "status":output_status,
            "detail":output_detail
        }
        return Response(context,status=res_status)

class ChangePasswordView(APIView):
    def post(self,request):
        user=request.user
        output_status=False
        output_detail="Falied"
        res_status=status.HTTP_400_BAD_REQUEST
        old_password=request.data.get("old_password")
        new_password=request.data.get("new_password")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            output_status=True
            output_detail="Password successfully changed"
            res_status=status.HTTP_200_OK
        else:
            output_detail="Wrong Password"
        context={
            "status":output_status,
            "detail":output_detail
        }
        return Response(context,status=res_status)


