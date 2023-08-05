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
        try:
            user = request.session.get('email')
            cust_obj = CustomUser.objects.get(email=user)
            print("cust_obj", cust_obj)
            context ={'user_is_authenticated': cust_obj.is_verified}
        except CustomUser.DoesNotExist:
            cust_obj= None
            context = {'user_is_authenticated': False}

        sub_category_id = request.query_params['sub_category']
        print("sub_category_id", sub_category_id)

        categories = Product.objects.filter(subcategoryName=sub_category_id,category=main_category_id)
        print("categories", categories)



        result_list = []
        for data in categories:

            try:
                print("cart item check")
                if cust_obj is not None:
                    cart = Cart.objects.get(user=cust_obj.id,product=data.id, orderid__isnull=True)
                    print("cart item is present in cart", cart)
                else:
                    print("user not login ")
                    cart = None
            except Cart.DoesNotExist:
                print("cart not exist")
                cart = None

            try:
                print("wishlist item check")
                if cust_obj is not None:
                    wish_status = WishList.objects.filter(user=cust_obj.id,product=data.id,add_to_cart=False).first()
                    print("cart item is present in cart", cart)
                else:
                    print("user not login ")
                    wish_status = None
            except WishList.DoesNotExist:
                print("WishList not exist")
                wish_status = None

            # images = [image.image.url for image in data.images.all()]
            image_url = data.images.first().image.url if data.images.exists() else None



            variants = []
            unique_sizes = set()
            get_variant = ProductVariant.objects.filter(product_id=data.id)

            for variant in get_variant:
                print("variant****", variant)
                if variant.quantity == 0 :
                    quantity_status = True
                else:
                    print("size add")
                    quantity_status = False
                    unique_sizes.add(variant.size)

                var_dict = {"size": variant.size,
                  "variant_id": variant.id,
                  "quantity_status": quantity_status}

                variants.append(var_dict)

            result_dict = {
                "product_id": data.id,
                "name": data.name,
                "description": data.description,
                "price": data.price,
                "images": [image_url] if image_url else [],
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

        context.update({"result_list": result_list})



        print("context", context)
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # If the request is made through JavaScript (AJAX), return a JSON response
            return JsonResponse(result_list, safe=False)
        else:
            # return render(request, 'products.html', context)
            return render(request, 'all_product.html', context)

class AllProductAPIList(APIView):

        def get(self, request):

            print("inside  product detail get", request)
            print("inside  product get", request.query_params)

            product_detail_id = request.query_params['product_id']
            print("product_detail_id", product_detail_id)
            try:
                user = request.session.get('email')
                cust_obj = CustomUser.objects.get(email=user)
                print("cust_obj", cust_obj)
                context = {'user_is_authenticated': cust_obj.is_verified}
            except CustomUser.DoesNotExist:
                cust_obj = None
                context = {'user_is_authenticated': False}

            print("product_detail_id", product_detail_id)
            categories = Product.objects.filter(id=product_detail_id)
            print("categories", categories)


            result_list = []
            for data in categories:

                try:
                    print("cart item check")
                    if cust_obj is not None:
                        cart = Cart.objects.get(user=cust_obj.id, product=data.id, orderid__isnull=True)
                        print("cart item is present in cart", cart)
                    else:
                        print("user not login ")
                        cart = None
                except Cart.DoesNotExist:
                    print("cart not exist")
                    cart = None

                try:
                    print("wishlist item check")
                    if cust_obj is not None:
                        wish_status = WishList.objects.filter(user=cust_obj.id, product=data.id, add_to_cart=False).first()
                        print("cart item is present in cart", cart)
                    else:
                        print("user not login ")
                        wish_status = None
                except WishList.DoesNotExist:
                    print("WishList not exist")
                    wish_status = None

                images = [image.image.url for image in data.images.all()]

                variants = []
                unique_sizes = set()
                get_variant = ProductVariant.objects.filter(product_id=data.id)

                for variant in get_variant:
                    if variant.quantity == 0:
                        quantity_status = True
                    else:
                        quantity_status = False
                        unique_sizes.add(variant.size)

                    var_dict = {"size": variant.size,

                                "variant_id": variant.id,
                                "quantity_status": quantity_status}

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
            context.update({"result_list": result_list})
            print("context", context)
            # if product_detail_id:
            #     if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            #         # If the request is made through JavaScript (AJAX), return a JSON response
            #         return JsonResponse(result_list, safe=False)
            #     else:
            #         return render(request, 'products.html', context)

            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

                return JsonResponse(result_list, safe=False)
            else:
                return render(request, 'products.html', context)






