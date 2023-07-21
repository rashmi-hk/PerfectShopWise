from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,EmailMultiAlternatives
from decouple import config
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
class VerifyOtpAPIList(APIView):

    def get(self,request):
        print("Inside  get   otp form")
        return render(request, 'otp_verification.html')
        # return render(request, 'new_lohin.html')

    def post(self,request):
        print("Inside otp post", request)
        print("Inside otp up", request.data)
        return