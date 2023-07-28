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
                get_variant = ProductVariant.objects.filter(product_id=product_obj.id)
                for variant in get_variant:
                    var_dict = {"size": variant.size,
                                "color": variant.color,
                                "variant_id": variant.id}
                    variants.append(var_dict)

                result_dict = {"product": item.product,
                               "price": item.product.price,
                               "product_variant": variant,
                               "product_id": item.product.id,
                               }
                if len(images) != 0:
                    result_dict.update({"images": images[0]})

                result_list.append(result_dict)

            context = {"result_list": result_list}

            print("context", context)
            return render(request, 'wishlist.html', context)

        except ObjectDoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)
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

        product_id = request.data['product_id']

        print("product_id", product_id)
        user = request.session.get('email')
        cust_obj = CustomUser.objects.get(email=user)

        try:
            wishlist_item = WishList.objects.filter(user=cust_obj,product=product_id).first()
            print("wishlist_item", wishlist_item)

            if wishlist_item:
                # Decrease the quantity by 1 if it's greater than 1
               wishlist_item.delete()

            return HttpResponse("Cart item deleted successfully.")

        except Cart.DoesNotExist:
            return HttpResponseBadRequest("Cart item not found.")


