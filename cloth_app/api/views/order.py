import datetime


from django.http import JsonResponse
from rest_framework.views import APIView
from ...models import CustomUser, Cart, OrderItem, Product,Order,ProductVariant

from django.shortcuts import render, redirect

from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


class OrderApiView(APIView):


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
                order.ordered_date =  datetime.datetime.now()
                order.save()



            return render(request, 'base.html')
        except ObjectDoesNotExist:
            response_data = {
                'success': False,
                'message': 'User with this email does not exist.',
            }
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)
