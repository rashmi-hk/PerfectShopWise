from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Categories,Subcategory
from django.http import JsonResponse
import os
# from ...serializers import ItemsSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging

LOGGER = logging.getLogger(__name__)

# Item api
class CategoryAPIList(APIView):

    def get(self, request,gender):
        print("inside  category_api", request.query_params)

        categories = Categories.objects.filter(gender=gender)
        context = {'categories': []}

        for category in categories:
            subcategories_data = []
            sub_cat_data = Subcategory.objects.filter(category=category.id)
            for item in sub_cat_data:
                subcategory_data = {
                    'subCategoryId':item.id,
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
            context['categories'].append(category_data)


        print("context", context)
        # return Response(context, status=status.HTTP_200_OK)
        return render(request, 'category.html', context)

