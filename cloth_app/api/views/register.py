from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,EmailMultiAlternatives
from decouple import config
from django.contrib.auth.hashers import make_password, check_password

# import os
# from ...serializers import CartSerializer
# from django.core import serializers
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
import concurrent.futures
from django.shortcuts import get_object_or_404
import json
import logging
import secrets
from django.utils import timezone
from datetime import timedelta

from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class RegisterAPIList(APIView):

    def get(self,request):
        print("Inside  get   register")
        return render(request, 'sign_up.html')
        # return render(request, 'new_lohin.html')

    def post(self,request):
        print("Inside sign up post", request)
        print("Inside sign up", request.data)
        if request.data:
            print("****", request.data["username"])
            otp = get_random_string(length=6, allowed_chars='1234567890')
            password = request.data["password"]
            username = request.data["username"]
            email = request.data["email"]
            phone_number = request.data["phone_number"]
            address = request.data["address"]
            otp = otp


            # Assuming 'user_dict' contains the necessary user information including 'email'
            user = CustomUser.objects.create_user(username=username, email=email,
                                                  password=password,otp=otp,phone_number=phone_number,address=address)

            print("db save password",user.password)
            # print("Created customer")
            # # to create a token
            # try:
            #     token = Token.objects.get(user=user)
            #     print("token get",token)
            # except Token.DoesNotExist:
            #     token = Token(user=user)
            #     print("token create", token)
            #
            # token.key = secrets.token_urlsafe(32)
            # token.created = timezone.now()
            # token.expires = token.created + timedelta(days=7)
            # token.save()

            # Send email with OTP asynchronously

            # Send email with OTP
            subject = 'Verify your email'
            message = f'Your OTP is {otp}'
            from_email = config('email_from')
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            # Redirect to verify page

            return render(request, 'otp_verification.html')

        # return HttpResponse('Notification sent successfully')