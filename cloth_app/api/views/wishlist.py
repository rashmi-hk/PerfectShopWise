from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Cart,ProductVariant,Product,CustomUser,WishList
from rest_framework import status
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist



# Item api
class WishListAPIList(APIView):

    def get(self, request):

        print("Inside get wishlist")
        try:
            user = request.session.get('email')
            cust_obj = CustomUser.objects.get(email=user)
            prod_obj = WishList.objects.filter(user=cust_obj, add_to_cart=False)


            result_list = []
            total_price = 0
            for item in prod_obj:
                print("product id", item.id)
                product_obj = Product.objects.get(id=item.product_id)
                print("product_obj", product_obj)
                images = [image.image.url for image in product_obj.images.all()]

                variants = []
                unique_sizes = set()

                get_variant = ProductVariant.objects.filter(product_id=product_obj.id)
                for variant in get_variant:
                    if variant.quantity == 0:
                         print("no product")
                    else:
                        print("Product present")
                        unique_sizes.add(variant.size)

                    var_dict = {"size": variant.size,

                                "variant_id": variant.id,
                                "product_quantity": variant.quantity,
                                }

                    variants.append(var_dict)


                result_dict = {"product": item.product,
                               "price": item.product.price,
                               "product_variant": variants,
                               "product_id": item.product.id,
                               "unique_sizes": unique_sizes,
                               "wishlist_id":item.id,
                               }
                if len(images) != 0:
                    result_dict.update({"images": images[0]})

                result_list.append(result_dict)

            context = {"result_list": result_list,
                       'user_is_authenticated': cust_obj.is_verified}
            if len(context['result_list']) == 0:
                return render(request, 'empty_wishlist.html',context={'user_is_authenticated': cust_obj.is_verified})
            else:

                print("context", context)
                return render(request, 'wishlist.html', context)

        except ObjectDoesNotExist:

            return render(request, 'empty_wishlist_without_login.html')
            # return JsonResponse({'prod_obj': cart_item_count}, status=status.HTTP_200_OK)

    def post(self, request):
        print("inside  wishlist api post  ", request)
        print("inside  wishlist api post  ", request.data)
        try:
            product_id = request.data['product_id']

            user = request.session.get('email')
            print("user", user)
            cust_obj = CustomUser.objects.get(email=user)
            prod_obj = Product.objects.get(id=product_id)
            cart_created_data = WishList.objects.create(user=cust_obj, product=prod_obj)
            if cart_created_data:

                response_data = {
                    'success': True,
                    'message': 'Product added to cart successfully.',
                    'cart_id': cart_created_data.id
                }

                return JsonResponse(response_data, status=status.HTTP_201_CREATED)
            else:
                # If the serializer validation fails, return the error details.
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)



    def delete(self, request):

        print("inside delete wish list item", request.data)

        wishlist_id = request.data['wishlist_id']

        print("wishlist_id", wishlist_id)
        user = request.session.get('email')
        cust_obj = CustomUser.objects.get(email=user)

        try:
            wishlist_item = WishList.objects.filter(user=cust_obj,id=wishlist_id).first()
            print("wishlist_item", wishlist_item)

            if wishlist_item:
                # Decrease the quantity by 1 if it's greater than 1
               wishlist_item.delete()

            return HttpResponse("Cart item deleted successfully.")

        except Cart.DoesNotExist:
            return HttpResponseBadRequest("Cart item not found.")






