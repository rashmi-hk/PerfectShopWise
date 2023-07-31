from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Product,ProductVariant,Cart,CustomUser,WishList
from django.http import JsonResponse
import os
# from ...serializers import ItemsSerializer
from django.core import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import logging
from django.http import HttpResponseBadRequest
from django.http import HttpResponse


# Item api
class ProductAPIList(APIView):

    def get(self, request):
        print("inside  product get", request)
        print("inside  product get", request.query_params)
        main_category_id = request.query_params['main_category']
        print("main_category_id", main_category_id)

        user = request.session.get('email')
        cust_obj = CustomUser.objects.get(email=user)
        print("cust_obj", cust_obj)

        sub_category_id = request.query_params['sub_category']
        print("sub_category_id", sub_category_id)

        categories = Product.objects.filter(subcategoryName=sub_category_id,category=main_category_id)
        print("categories", categories)



        result_list = []
        for data in categories:

            try:
                print("cart item check")
                cart = Cart.objects.get(user=cust_obj.id,product=data.id, orderid__isnull=True)
                print("cart item is present in cart", cart)
            except Cart.DoesNotExist:
                print("cart not exist")
                cart = None

            try:
                print("wishlist item check")
                wish_status = WishList.objects.filter(user=cust_obj.id,product=data.id,add_to_cart=False).first()
                print("cart item is present in cart", cart)
            except WishList.DoesNotExist:
                print("WishList not exist")
                wish_status = None

            images = [image.image.url for image in data.images.all()]

            variants = []
            unique_sizes = set()
            get_variant = ProductVariant.objects.filter(product_id=data.id)

            for variant in get_variant:
                if variant.quantity == 0 :
                    quantity_status = True
                else:
                    quantity_status = False

                var_dict = {"size": variant.size,
                 "color": variant.color,
                  "variant_id": variant.id,
                  "quantity_status": quantity_status}
                unique_sizes.add(variant.size)
                variants.append(var_dict)

            result_dict = {
                "product_id": data.id,
                "name": data.name,
                "description": data.description,
                "price": data.price,
                "images": images,
                "variants": variants,
                "unique_sizes": unique_sizes,
            }
            if cart is not None:
                result_dict.update({"disable": True})
            else:
                result_dict.update({"disable": False})

            if wish_status is not None:
                result_dict.update({"wish_status_disable": True})
            else:
                result_dict.update({"wish_status_disable": False})

            result_list.append(result_dict)
        # return Response(context=result_list, status=status.HTTP_200_OK)
        context = {"result_list": result_list}
        print("context", context)
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # If the request is made through JavaScript (AJAX), return a JSON response
            return JsonResponse(result_list, safe=False)
        else:
            return render(request, 'products.html', context)
        # return JsonResponse(result_list, safe=False)

