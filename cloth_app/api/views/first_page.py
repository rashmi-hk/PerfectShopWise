from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser,Categories,Subcategory
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
                'user_is_authenticated': cust_obj.is_verified,
                'category_data': data_list,
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