from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
# import os
# from ...serializers import CartSerializer
# from django.core import serializers

from django.shortcuts import get_object_or_404
import json
import logging

from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class HomeAPIList(APIView):

    def get(self,request):
        print("Inside get homeapi")
        # return render(request, 'base.html')
        # return render(request, 'email_templet.html')
        # return render(request, 'forgot_password.html')
        # return render(request, 'reset_password.html')
        # return render(request, 'index.html')
        return render(request, 'login.html')
        # return render(request, 'otp_verification.html')

    def post(self,request):
        print("Inside home post", request)
        print("Inside home post", request.data)
        try:
            email = request.data['email']

            password = request.data['password']
            print("password type", type(password))
            customer = CustomUser.objects.get(email=email)  # Assuming User is the user model you are using
            print("customer", customer)
            print("password", customer.password)
            print("password type", type(customer.password))
            password_matched = check_password(password, customer.password)
            print("password_matched", password_matched)

            if not password_matched:
                print("invalid")

                return render(request, 'login_custom.html', {'error_message': 'Invalid credentials'})
            else:
                print("valid")
                request.session['customer_id'] = customer.id
                request.session['email'] = email
                return_list = []
            return redirect('cart')
        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'}, status=404)
