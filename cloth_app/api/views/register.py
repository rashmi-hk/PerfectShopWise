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
from rest_framework import status
from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class RegisterAPIList(APIView):

    def get(self,request,variant=None):
        print("Inside  get   register")
        if variant:
            user = request.session.get('email')
            cust_obj = CustomUser.objects.get(email=user)
            result_dict = {"name": cust_obj.username,
                           "phone_number": cust_obj.phone_number,
                           "address": cust_obj.address,
                           "user_id": cust_obj.id,
                           }
            context = {"result_dict": result_dict,
                       'user_is_authenticated': cust_obj.is_verified,
                       }
            return render(request, 'user_profile.html', context=context)
        else:
            return render(request, 'sign_up.html')
        # return render(request, 'new_lohin.html')

    def post(self,request):
        print("Inside sign up post", request)
        print("Inside sign up", request.data)
        try:
            if request.data:
                print("****", request.data["username"])
                otp = get_random_string(length=6, allowed_chars='1234567890')
                password = request.data["password"]
                username = request.data["username"]
                email = request.data["email"]
                phone_number = request.data["phone_number"]
                address = request.data["address"]
                otp = otp

                check_existence = CustomUser.objects.filter(email=email).first()
                if not check_existence:
                    # Assuming 'user_dict' contains the necessary user information including 'email'
                    user = CustomUser.objects.create_user(username=username, email=email,
                                                          password=password,otp=otp,phone_number=phone_number,address=address)

                    print("db save password",user.password)


                    # Send email with OTP
                    subject = 'Verify your email'
                    message = f'Your OTP is {otp}'
                    from_email = config('email_from')
                    recipient_list = [email]
                    send_mail(subject, message, from_email, recipient_list)
                    # Redirect to verify page
                    context = {"email": email}
                    return render(request, 'otp_verification.html', context)
                else:
                    error_message = 'CustomUser with this email id already exist,Please try with different one'
                    return render(request, 'sign_up.html', {'error_message': error_message})
        except  Exception as e:
            print(f"An unexpected error occurred: {e}")

    def patch(self, request):

        try:
            print("register patch ", request.data)
            user_id = request.data['user_id']
            name = request.data['name']
            phone_number = request.data['phone_number']
            address = request.data['address']

            user = CustomUser.objects.get(id=user_id)
            if name:
                user.username = name
            if phone_number:
                user.phone_number = phone_number
            if address:
                user.address = address

                # Save the updated user data
            user.save()

            return Response(status=status.HTTP_200_OK)
        except  Exception as e:
            print(f"An unexpected error occurred: {e}")

# return HttpResponse('Notification sent successfully')