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
class FirstPageAPIList(APIView):

    def get(self,request):
        print("Inside get homeapi")
        return render(request, 'base.html')
