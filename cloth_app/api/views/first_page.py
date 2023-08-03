from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
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
class FirstPageAPIList(APIView):

    def get(self, request):
        print("Inside get first page")

        try:
            user = request.session.get('email')
            print("user", user)
            cust_obj = CustomUser.objects.get(email=user)
            print("cust_obj", cust_obj)

            context = {
                'user_is_authenticated': cust_obj.is_verified,
            }
            print("context", context)
            return render(request, 'base.html', context)
        except ObjectDoesNotExist:
            # Handle the case when the CustomUser object doesn't exist
            context = {
                'user_is_authenticated': False,
            }
            print("context", context)
            return render(request, 'base.html', context)