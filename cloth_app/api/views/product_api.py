from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Product,ProductVariant
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
class ProductAPIList(APIView):

    def get(self, request):
        print("inside  product get", request)
        print("inside  product get", request.query_params)
        main_category_id = request.query_params['main_category']
        print("main_category_id", main_category_id)

        sub_category_id = request.query_params['sub_category']
        print("sub_category_id", sub_category_id)

        categories = Product.objects.filter(subcategoryName=sub_category_id,category=main_category_id)
        print("categories", categories)


        result_list = []
        for data in categories:
            images = [image.image.url for image in data.images.all()]

            variants = []
            get_variant = ProductVariant.objects.filter(product_id=data.id)
            for variant in get_variant:
                var_dict = {"size": variant.size,
                 "color": variant.color}
                variants.append(var_dict)

            result_dict = {
                "name": data.name,
                "description": data.description,
                "price": data.price,
                "images": images,
                "variants": variants
            }
            result_list.append(result_dict)
        # return Response(context=result_list, status=status.HTTP_200_OK)
        context = {"result_list": result_list}
        print("context", context)
        return render(request, 'products.html', context)
        # return JsonResponse(result_list, safe=False)

