from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Cart,ProductVariant,Product,CustomUser,WishList
from rest_framework import status
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


# Item api
class CartAPIList(APIView):

    def get(self,request):
        try:
            print("Inside get cart")
            print("Inside  get   register")
            user = request.session.get('email')
            cust_obj = CustomUser.objects.get(email=user)
            prod_obj = Cart.objects.filter(user=cust_obj,orderid_id__isnull=True)

            cart_item_count = prod_obj.count()


            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                print("HI  in X0request ",cust_obj.username)
                return JsonResponse({'prod_obj': cart_item_count,
                                     'user_name': cust_obj.username,
                                     'user_is_authenticated': cust_obj.is_verified}, status=status.HTTP_200_OK)
            else:
                result_list = []
                total_price = 0
                discounted_total_price = 0
                for item in prod_obj:

                    print("product id", item.id)
                    product_obj = Product.objects.get(id =item.product_id)
                    print("product_obj",product_obj)
                    images = [image.image.url for image in product_obj.images.all()]
                    total_price += item.product.price * item.quantity
                    discount_percent =  item.product.offer
                    print("discount_percent", discount_percent)

                    get_variant = ProductVariant.objects.filter(product_id=product_obj.id)
                    unique_sizes = set()
                    for variant in get_variant:
                        if variant.quantity == 0:
                            quantity_status = True
                        else:
                            quantity_status = False
                            unique_sizes.add(variant.size)


                    discounted_price = item.product.price * (1 - (discount_percent / 100))
                    print("discounted_price", discounted_price)
                    discounted_total_price += discounted_price * item.quantity
                    result_dict = {"product": item.product,
                                   "price": item.product.price,
                                   "product_variant": item.product_variant,
                                   "quantity": item.quantity,
                                   "product_id": item.product.id,
                                   "discounted_price": round(discounted_price),
                                   "unique_sizes":unique_sizes,
                                   "product_variant_id": item.product_variant.id,
                                   "discount_percent": round(discount_percent),
                                   }
                    if len(images) != 0:
                        result_dict.update({"images": images[0]})

                    result_list.append(result_dict)

                context = {"result_list": result_list,
                           "total_price": round(total_price),
                           "discounted_total_price":round(discounted_total_price),
                           'user_name': cust_obj.username,
                           'user_is_authenticated': cust_obj.is_verified}

                print("context", context)
                if len(context['result_list']) != 0:
                    print("normal")
                    return render(request, 'cart.html', context)
                else:
                    print("with login")
                    return render(request, 'empty_cart.html', context)
        # return JsonResponse({'prod_obj': cart_item_count}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            print("without login")
            context = {'user_is_authenticated': False}
            return render(request, 'empty_cart_without_login.html', context)

    def post(self, request):
        print("inside  cart api post  ",request)
        print("inside  cart api post  ",request.data)
        try:
            product_id = request.data['product_id']

            product_size = request.data['size_variants']

            print("product_id,product_size,product_color",product_id,product_size)
            user = request.session.get('email')
            print("user", user)
            cust_obj = CustomUser.objects.get(email=user)
            print("cust_obj", cust_obj)
            prod_obj = Product.objects.get(id=product_id)
            print("prod_obj", prod_obj)
            product_vartaint_obj = ProductVariant.objects.get(product=prod_obj,size=product_size)
            print("product_vartaint_obj", product_vartaint_obj)

            cart_item_exist = Cart.objects.filter(user=cust_obj, product=product_id,product_variant=product_vartaint_obj,
                                                cart_created=True,
                                                orderid__isnull=True).first()

            if cart_item_exist:
                print("Item already exist so update")
                cart_item = cart_item_exist  # Assuming there's only one item per table
                cart_item.quantity += 1
                cart_item.save()

                response_data = {
                    'success': True,
                    'message': 'Product updated to cart successfully.',
                    'cart_id': cart_item_exist.id,  # If you want to return the cart ID to the client
                    # If you want to return the cart total to the client
                    # Add any other cart-related data that you want to return to the client
                }
                return JsonResponse(response_data, status=status.HTTP_200_OK)
            else:

                cart_created_data = Cart.objects.create(user=cust_obj,product=prod_obj,product_variant=product_vartaint_obj, cart_created=True)
                print("cart_created_data", cart_created_data)
                if cart_created_data:

                    response_data = {
                        'success': True,
                        'message': 'Product added to cart successfully.',
                        'cart_id': cart_created_data.id,  # If you want to return the cart ID to the client
                         # If you want to return the cart total to the client
                        # Add any other cart-related data that you want to return to the client
                    }

                    return JsonResponse(response_data, status=status.HTTP_201_CREATED)
                else:
                    # If the serializer validation fails, return the error details.
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist :
            response_data = {
                'success': False,
                'message': 'User with this email does not exist.',
            }
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request):

        print("inside delete cart item", request.data)

        product_id = request.data['product_id']

        print("product_id", product_id)
        user = request.session.get('email')
        cust_obj = CustomUser.objects.get(email=user)

        product_size = request.data.get('size')
        print("product_size", product_size)

        product_vartaint_obj = ProductVariant.objects.get(product=product_id, size=product_size)
        print("product_vartaint_obj", product_vartaint_obj)

        try:
            cart_item = Cart.objects.filter(user=cust_obj,product=product_id, product_variant=product_vartaint_obj,cart_created=True,orderid__isnull=True).first()
            print("cart_item", cart_item)

            if cart_item:
                # Decrease the quantity by 1 if it's greater than 1
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()

            return HttpResponse("Cart item deleted successfully.")

        except Cart.DoesNotExist:
            return HttpResponseBadRequest("Cart item not found.")

    def patch(self, request):

        try:
            print("cart patch request", request.data)
            print("cart patch request", request.data.get)
            product_id =  request.data.get('product_id')
            print("product_id", product_id)

            user = request.session.get('email')
            cust_obj = CustomUser.objects.get(email=user)

            prod_obj = Product.objects.get(id=product_id)
            print("prod_obj", prod_obj)
            product_size = request.data.get('size')
            print("product_size", product_size)

            product_vartaint_obj = ProductVariant.objects.get(product=prod_obj, size=product_size)
            print("product_vartaint_obj", product_vartaint_obj)


            cart_items = Cart.objects.filter(user=cust_obj,product=product_id, product_variant=product_vartaint_obj,cart_created=True,orderid__isnull=True).first()
            print("cart_items", cart_items)
            wishlist_id = request.data.get('wishlist_id')
            if cart_items and wishlist_id:
                print("Inside if ")
                cart_item = cart_items  # Assuming there's only one item per table
                cart_item.quantity += 1
                cart_item.save()
                print("updated and set status to wishlist ")
                wish_obj = WishList.objects.filter(user=cust_obj, id=wishlist_id).first()
                wish_obj.add_to_cart = True
                wish_obj.save()

            elif cart_items:
                print("Inside if ")
                cart_item = cart_items  # Assuming there's only one item per table
                cart_item.quantity += 1
                cart_item.save()
                print("updated")

            else:


                wishlist_id = request.data.get('wishlist_id')
                print("product_size", product_size)



                cart_created_data = Cart.objects.create(user=cust_obj, product=prod_obj,
                                                        product_variant=product_vartaint_obj, cart_created=True)

                wish_obj = WishList.objects.filter(user=cust_obj,id=wishlist_id).first()
                wish_obj.add_to_cart = True
                wish_obj.save()

            return JsonResponse({'message': 'Cart quantity updated successfully'})
        except Cart.DoesNotExist:
                return JsonResponse({'error': 'Cart not found'}, status=404)
        except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)
        except ProductVariant.DoesNotExist:
                return JsonResponse({'error': 'ProductVariant not found'}, status=404)
        except Exception as e:
            # Catch any other general exceptions here
            # You can log the error for debugging purposes
            print('Unexpected error occurred:', str(e))
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

class UserCheckAPIList(APIView):
    def get(self,request):
        print("UserCheckAPIList  inside ***************************** ")
        try:
            user_email = request.session.get('email')
            if user_email:
                print("I am hear")
                cust_obj = get_object_or_404(CustomUser, email=user_email)
                return JsonResponse({'user_is_authenticated': cust_obj.is_verified}, status=status.HTTP_200_OK)
            else:
                print("in else")
                return JsonResponse({'user_is_authenticated': False}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            print("in except")
            return JsonResponse({'user_is_authenticated': False}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle other exceptions here, log them, or return an appropriate error response
            return JsonResponse({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):

        try:
            print("inside UserCheckAPIList *******************^^^^^^^^^^^^^", request)
            print("inside UserCheckAPIList *******************^^^^^^^^^^^^^", request.data)
            print("cart patch request", request.data.get)
            product_id = request.GET.get('product_id')
            print("product_id", product_id)

            size = request.data.get('size')
            print("size", size)

            user = request.session.get('email')
            cust_obj = CustomUser.objects.get(email=user)
            size = request.data.get('size')
            print("size", size)
            cart_items = Cart.objects.filter(user=cust_obj, product=product_id, cart_created=True,
                                             orderid__isnull=True).first()

            product_vartaint_obj = ProductVariant.objects.get(product=product_id, size=size)
            print("product_vartaint_obj", product_vartaint_obj)

            print("cart_items", cart_items)
            if cart_items:
                cart_item = cart_items  # Assuming there's only one item per table
                cart_item.product_variant = product_vartaint_obj
                cart_item.save()
            return JsonResponse({'message': 'Size updated successfully'})
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except ProductVariant.DoesNotExist:
            return JsonResponse({'error': 'ProductVariant not found'}, status=404)






