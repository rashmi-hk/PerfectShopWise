import datetime

from django.db.models import F
from django.http import JsonResponse
from rest_framework.views import APIView
from ...models import CustomUser, Cart, OrderItem, Product,Order,ProductVariant

from django.shortcuts import render, redirect

from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


class OrderApiView(APIView):

    def get(self, request):
        print("Inside order get")
        try:
            user = request.session.get('email')
            print("user", user)
            cust_obj = CustomUser.objects.get(email=user)
            print("cust_obj", cust_obj)

            product_variants = ProductVariant.objects.filter(
                orderitem__order__user=cust_obj
            )
            print("product_variants",product_variants)
            print("product_variants",len(product_variants))
            # Get the product images for each product variant
            product_images = []
            for variant in product_variants:
                # Retrieve the product images for the variant
                images = variant.product.images.all()

                # If there are multiple images, you may want to select one as the main image.
                # For example, if you want to select the first image, you can do this:
                main_image = images.first() if images else None
                order_statuses = Order.objects.filter(orderitem__product_variant=variant,user=cust_obj.id).values_list('status',
                                                                                                              flat=True).first()
                # Append the product name, size, color, and main image URL (if available) to the result list
                product_images.append({
                    'product_name': variant.product.name,
                    'size': variant.get_size_display(),
                    'color': variant.color,
                    'status': order_statuses,
                    'main_image_url': main_image.image.url if main_image else None,
                })
                print("product_images", product_images)
            context = {"product_images": product_images}
            print("product_images", product_images)
            if len(product_variants) == 0:
                context["error_message"] = "No product images available."

            print("context********************************",context)

            return render(request, 'order_history.html', context)
        except ObjectDoesNotExist:
            response_data = {
                'success': False,
                'message': 'User with this email does not exist.',
            }
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        print("Inside api Order post", request.data)
        total_price = 0
        try:
            print("Inside try")
            user = request.session.get('email')
            cust_obj = CustomUser.objects.get(email=user)

            with transaction.atomic():
                order = Order.objects.create(user=cust_obj,total_price=0)

                cart_items = Cart.objects.filter(user=cust_obj,orderid_id__isnull=True)
                print("cart_items", cart_items)
                # cart :-   product, product_variant, quantity, orderid
                # order_item:- order, product_variant, quantity
                order_items = []
                for cart_item in cart_items:
                    print("cart_item.id", cart_item)
                    item_price = cart_item.product.price
                    print("item_price", item_price)

                    product_id = cart_item.product.id
                    print("product_id", product_id)

                    prod_obj = Product.objects.get(id=product_id)

                    quantity = cart_item.quantity
                    print("quantity", quantity)

                    product_variant=cart_item.product_variant
                    print("product_variant", product_variant)


                    # item_price = item.itemPrice
                    order_item_price = quantity * item_price
                    print("order_item_price", order_item_price)

                    # Create an Order_Items object
                    order_item = OrderItem.objects.create(quantity=quantity, order_item_price=order_item_price,
                                                            product=prod_obj,product_variant=product_variant,order=order)

                    print("order_item", order_item)

                    order_items.append(order_item)
                    total_price += order_item_price

                    Cart.objects.filter(user=cust_obj, orderid_id__isnull=True).update(orderid=order_item.order.id)

                    print("update", cart_item)
                    print("update", cart_item.orderid)

                    product_variant_obj = ProductVariant.objects.get(id=product_variant.id,size=product_variant.size,color=product_variant.color)
                    print("product_variant_obj", product_variant_obj)

                    if product_variant_obj.quantity > 1:
                        product_variant_obj.quantity -= 1
                        product_variant_obj.save()
                    else:
                        product_variant_obj.quantity = 0
                        product_variant_obj.save()

                order.total_price = total_price
                order.is_ordered = True
                order.status = 'PROCESSING'
                order.ordered_date =  datetime.datetime.now()
                order.save()



            return render(request, 'base.html')
        except ObjectDoesNotExist:
            response_data = {
                'success': False,
                'message': 'User with this email does not exist.',
            }
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)
