from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser,OrderItem
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from ...models import ProductVariant, Order
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password

class AdminUtilityAPIList(APIView):

    def get(self, request):
        response_data = {}

        try:
            print("request", request)
            admin_password = request.query_params['password']
            print("admin_password", admin_password)

            email = request.query_params['email']
            print("email", email)
            try:


                user = CustomUser.objects.get(email=email)
                print("user obj",user)
                a = check_password(admin_password, user.password)
                print("AAA", a)
                print(user.is_superuser)
            except CustomUser.DoesNotExist:
                user = None
            if user is not None and check_password(admin_password, user.password) and user.is_superuser:
                # Total number of orders placed today
                today = timezone.now().date()
                total_orders_placed_obj = Order.objects.filter(ordered_date__date=today)
                for data in total_orders_placed_obj:
                    print("total_orders_placed_obj*******", data.id)
                total_orders_placed = total_orders_placed_obj.count()
                print("total_orders_placed", total_orders_placed)
                response_data['total_orders_placed'] = total_orders_placed

                # Total number of products per size and color for today's orders
                product_variants_per_size_color = ProductVariant.objects.filter(
                    orderitem__order__ordered_date__date=today
                ).values('size',  'product__name').annotate(
                    total_products=Count('id')
                )

                products_per_size_color = []
                for variant in product_variants_per_size_color:
                    products_per_size_color.append({
                        'size': variant['size'],

                        'product_name': variant['product__name'],
                        'total_products': variant['total_products'],
                    })

                response_data['products_per_size_color'] = products_per_size_color

                # Quantity left in stock per product variant for today
                one_day_ago = today - timedelta(days=1)
                products_with_stock_left_per_day = ProductVariant.objects.annotate(
                    quantity_left=F('quantity') - Sum('orderitem__quantity', filter=Q(orderitem__order__ordered_date__gte=one_day_ago))
                ).values('product__name', 'size', 'quantity_left')

                stock_left_per_day = []
                for product in products_with_stock_left_per_day:
                    stock_left_per_day.append({
                        'product_name': product['product__name'],
                        'size': product['size'],

                        'quantity_left': product['quantity_left']
                    })

                response_data['stock_left_per_day'] = stock_left_per_day

                # Quantity left in stock per product variant for the entire month
                first_day_of_month = today.replace(day=1)
                one_month_ago = first_day_of_month - timedelta(days=1)
                products_with_stock_left_per_month = ProductVariant.objects.annotate(
                    quantity_left=F('quantity') - Sum('orderitem__quantity', filter=Q(orderitem__order__ordered_date__gte=one_month_ago))
                ).values('product__name', 'size','quantity_left')

                stock_left_per_month = []
                for product in products_with_stock_left_per_month:
                    stock_left_per_month.append({
                        'product_name': product['product__name'],
                        'size': product['size'],

                        'quantity_left': product['quantity_left']
                    })

                response_data['stock_left_per_month'] = stock_left_per_month

                # Total number of orders placed this month
                total_orders_this_month = Order.objects.filter(ordered_date__date__month=today.month).count()
                response_data['total_orders_this_month'] = total_orders_this_month

                # Total number of products per size and color for this month's orders
                product_variants_per_size_color_month = ProductVariant.objects.filter(
                    orderitem__order__ordered_date__date__month=today.month
                ).values('size', 'product__name').annotate(
                    total_products=Count('id')
                )

                products_per_size_color_month = []
                for variant in product_variants_per_size_color_month:
                    products_per_size_color_month.append({
                        'size': variant['size'],

                        'product_name': variant['product__name'],
                        'total_products': variant['total_products'],
                    })

                response_data['products_per_size_color_month'] = products_per_size_color_month
                request.session['customer_id'] = user.id
                request.session['email'] = email

                return render(request, 'admin_utility.html', response_data)
            else:
                print("invalid")
                messages.error(request, 'Invalid credentials')  # Add error message to Django messages framework

                # Pass the error message to the template
                return render(request, 'admin_utiliti_login.html', {'error_message': 'Invalid credentials'})


        except Exception as e:
            response_data['error'] = str(e)
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminUtilityLoginAPIList(APIView):

        def get(self, request):
            print("Inside AdminUtilityLoginAPIList")



            # Pass the error message to the template
            return render(request, 'admin_utiliti_login.html')



class AdminUtilityOrderAPIList(APIView):

    def get(self, request):
        orders = Order.objects.all()
        order_items_grouped = {}

        for order in orders:
            final_discounted_price = 0
            total_price = 0
            order_items = OrderItem.objects.filter(order=order)
            print("order_items ***************", order_items)
            order_item_details = []

            discount_percent = 0
            discount_price = 0
            for order_item in order_items:
                product_variant = order_item.product_variant
                discount_percent = product_variant.product.offer
                discounted_item_price = order_item.order_item_price * (1 - (discount_percent / 100))
                print("discounted_item_price", discounted_item_price)
                discount_price = discounted_item_price
                total_price += order_item.order_item_price * order_item.quantity
                order_item_detail = {
                    "product_variant": order_item.product_variant,
                    "quantity": order_item.quantity,
                    "order_item_price": order_item.order_item_price,
                    "discount": discount_price,
                    "offer": round(discount_percent),
                    # Add more fields if needed
                }
                order_item_details.append(order_item_detail)
                final_discounted_price += (discount_price * order_item.quantity)

            #     print("discount_percent", discount_percent)


            #     print("discounted_price", discounted_price)
            order_items_grouped[order.id] = {
                "order_details": {
                    "user": order.user.username,
                    "ordered_date": order.ordered_date,
                    "Total_amount": round(total_price),
                    "discount_amount":round(final_discounted_price),
                    # Add more order details if needed
                },
                "order_items": order_item_details,
            }

        context = {"order_items_grouped": order_items_grouped}
        print("context", context)
        return render(request, 'admin_utiliti_order.html', context)

    # def get(self, request):
    #     response_data = {}
    #
    #
    #     print("request", request)
    #     total_price = 0
    #     # try:
    #     # total_orders_placed_obj = Order.objects.all()
    #     # for data in total_orders_placed_obj:
    #     #     order_details = OrderItem.objects.filter(order=data.id)
        #     prod_list = []
        #     for order_item in order_details:
        #         dict_data = {
        #             "user_name":user.username,
        #             "order_quantity": order_item.quantity,
        #             "product_variant": order_item.product_variant,
        #             "order_item_price": order_item.order_item_price}
        #
        #         prod_list.append({order_details.id: dict_data})
        #     product_variants_per_size = ProductVariant.objects.filter(product=data.id)
        #
        #     size = len(product_variants_per_size)
        #     products_per_size = []
        #
        #
        #         # item_price = item.itemPrice
        #     order_item_price = data.quantity * data.item_price
        #     print("order_item_price", order_item_price)
        #     total_price += order_item_price
        #
        #     discount_percent = data.product.offer
        #     print("discount_percent", discount_percent)
        #
        #     discounted_price = order_item_price * (1 - (discount_percent / 100))
        #     print("discounted_price", discounted_price)
        #
        #     response_data['products_per_size'] = products_per_size
        #     response_data['user_name'] = data.user.username
        #     response_data['ordered_date'] = data.ordered_date
        #     response_data['total'] = discounted_price
        #     response_data['size'] = size
        #     print("discounted_price",discounted_price)

        # except Exception as e:
        #     response_data['error'] = str(e)
        #     return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # order_details = OrderItem.objects.select_related('order', 'order__user').all()
        # prod_list = []
        # for order_item in order_details:
        #     # Access the related Order and User instances
        #     order = order_item.order
        #     user = order.user  # Assuming the related User field in the Order model is named 'user'
        #
        #     # Access the fields you want from the Order and OrderItem models
        #     dict_data = {
        #                "order_quantity" : order_item.quantity,
        #                "product_variant":order_item.product_variant,
        #                "order_item_price": order_item.order_item_price}
        #
        #
        #     prod_list.append({user.username:dict_data})
        # context = {"prod_list":prod_list}
        # print("context",context)
        #
        #     # Now you can use the 'username' and 'order_quantity' variables as needed
        #     # print(f"Username: {username}, Order Quantity: {order_quantity}")
        #
        # return render(request, 'admin_utiliti_order.html', context)
        #




