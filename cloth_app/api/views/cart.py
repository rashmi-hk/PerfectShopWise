from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import Cart,ProductVariant,Product,CustomUser,WishList
from rest_framework import status
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist



# Item api
class CartAPIList(APIView):

    def get(self,request):

        print("Inside get cart")
        print("Inside  get   register")
        user = request.session.get('email')
        cust_obj = CustomUser.objects.get(email=user)
        prod_obj = Cart.objects.filter(user=cust_obj,orderid_id__isnull=True)

        cart_item_count = prod_obj.count()


        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print("HI")
            return JsonResponse({'prod_obj': cart_item_count}, status=status.HTTP_200_OK)
        else:
            result_list = []
            total_price = 0
            for item in prod_obj:
                print("product id", item.id)
                product_obj = Product.objects.get(id =item.product_id)
                print("product_obj",product_obj)
                images = [image.image.url for image in product_obj.images.all()]
                total_price += item.product.price * item.quantity
                result_dict = {"product": item.product,
                               "price": item.product.price,
                               "product_variant": item.product_variant,
                               "quantity": item.quantity,
                               "product_id": item.product.id,
                               }
                if len(images) != 0:
                    result_dict.update({"images": images[0]})

                result_list.append(result_dict)

            context = {"result_list": result_list,
                       "total_price": total_price}

            print("context", context)
            return render(request, 'cart.html', context)
        # return JsonResponse({'prod_obj': cart_item_count}, status=status.HTTP_200_OK)

    def post(self, request):
        print("inside  cart api post  ",request)
        print("inside  cart api post  ",request.data)
        try:
            product_id = request.data['product_id']

            product_size = request.data['size_variants']
            product_color = request.data['color_variants']
            print("product_id,product_size,product_color",product_id,product_size,product_color)
            user = request.session.get('email')
            print("user", user)
            cust_obj = CustomUser.objects.get(email=user)
            print("cust_obj", cust_obj)
            prod_obj = Product.objects.get(id=product_id)
            print("prod_obj", prod_obj)
            product_vartaint_obj = ProductVariant.objects.get(product=prod_obj,size=product_size,color=product_color)
            print("product_vartaint_obj", product_vartaint_obj)
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

        try:
            cart_item = Cart.objects.filter(user=cust_obj,product=product_id, cart_created=True,orderid__isnull=True).first()
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

            cart_items = Cart.objects.filter(user=cust_obj,product=product_id, cart_created=True,orderid__isnull=True).first()
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
                product_size = request.data.get('size')
                product_color = request.data.get('color')
                wishlist_id = request.data.get('wishlist_id')
                print("product_size", product_size)
                print("product_color", product_color)

                prod_obj = Product.objects.get(id=product_id)
                print("prod_obj", prod_obj)
                product_vartaint_obj = ProductVariant.objects.get(product=prod_obj, size=product_size,
                                                                  color=product_color)
                print("product_vartaint_obj", product_vartaint_obj)

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




