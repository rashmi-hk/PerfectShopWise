from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser
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
                total_orders_placed = total_orders_placed_obj.count()
                print("total_orders_placed", total_orders_placed)
                response_data['total_orders_placed'] = total_orders_placed

                # Total number of products per size and color for today's orders
                product_variants_per_size_color = ProductVariant.objects.filter(
                    orderitem__order__ordered_date__date=today
                ).values('size', 'color', 'product__name').annotate(
                    total_products=Count('id')
                )

                products_per_size_color = []
                for variant in product_variants_per_size_color:
                    products_per_size_color.append({
                        'size': variant['size'],
                        'color': variant['color'],
                        'product_name': variant['product__name'],
                        'total_products': variant['total_products'],
                    })

                response_data['products_per_size_color'] = products_per_size_color

                # Quantity left in stock per product variant for today
                one_day_ago = today - timedelta(days=1)
                products_with_stock_left_per_day = ProductVariant.objects.annotate(
                    quantity_left=F('quantity') - Sum('orderitem__quantity', filter=Q(orderitem__order__ordered_date__gte=one_day_ago))
                ).values('product__name', 'size', 'color', 'quantity_left')

                stock_left_per_day = []
                for product in products_with_stock_left_per_day:
                    stock_left_per_day.append({
                        'product_name': product['product__name'],
                        'size': product['size'],
                        'color': product['color'],
                        'quantity_left': product['quantity_left']
                    })

                response_data['stock_left_per_day'] = stock_left_per_day

                # Quantity left in stock per product variant for the entire month
                first_day_of_month = today.replace(day=1)
                one_month_ago = first_day_of_month - timedelta(days=1)
                products_with_stock_left_per_month = ProductVariant.objects.annotate(
                    quantity_left=F('quantity') - Sum('orderitem__quantity', filter=Q(orderitem__order__ordered_date__gte=one_month_ago))
                ).values('product__name', 'size', 'color', 'quantity_left')

                stock_left_per_month = []
                for product in products_with_stock_left_per_month:
                    stock_left_per_month.append({
                        'product_name': product['product__name'],
                        'size': product['size'],
                        'color': product['color'],
                        'quantity_left': product['quantity_left']
                    })

                response_data['stock_left_per_month'] = stock_left_per_month

                # Total number of orders placed this month
                total_orders_this_month = Order.objects.filter(ordered_date__date__month=today.month).count()
                response_data['total_orders_this_month'] = total_orders_this_month

                # Total number of products per size and color for this month's orders
                product_variants_per_size_color_month = ProductVariant.objects.filter(
                    orderitem__order__ordered_date__date__month=today.month
                ).values('size', 'color', 'product__name').annotate(
                    total_products=Count('id')
                )

                products_per_size_color_month = []
                for variant in product_variants_per_size_color_month:
                    products_per_size_color_month.append({
                        'size': variant['size'],
                        'color': variant['color'],
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

