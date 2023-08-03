from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from ...models import Categories,Subcategory
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
        return render(request, 'login.html')


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

                categories = Categories.objects.all()

                data_list = []
                for category in categories:
                    subcategories_data = []
                    sub_cat_data = Subcategory.objects.filter(category=category.id)
                    for item in sub_cat_data:
                        subcategory_data = {
                            'subCategoryId': item.id,
                            'subcategoryName': item.subcategoryName,
                            'sub_category_img': item.sub_category_img.url if item.sub_category_img else None,
                        }
                        subcategories_data.append(subcategory_data)

                    category_data = {
                        'categoryId': category.id,
                        'categoryName': category.categoryName,
                        'category_img': category.category_img.url if category.category_img else None,
                        'subcategories': subcategories_data,
                    }
                    data_list.append(category_data)

                context = {
                    'user_is_authenticated': customer.is_verified,
                    'category_data': data_list,
                }
                print("context", context)
            return render(request, 'base.html', context)
        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'}, status=404)
