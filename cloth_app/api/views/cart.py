from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,EmailMultiAlternatives
from decouple import config



# Item api
class CartAPIList(APIView):

    def get(self,request):
        print("Inside  get   register")
        f = request.session.get('email')
        print("f", f)
        return render(request, 'sign_up.html')
        # return render(request, 'new_lohin.html')

