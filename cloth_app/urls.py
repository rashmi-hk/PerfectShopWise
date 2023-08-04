from django.urls import path
from cloth_app.api.views.home import HomeAPIList
from cloth_app.api.views.categories import CategoryAPIList
from cloth_app.api.views.product_api import ProductAPIList,AllProductAPIList
from cloth_app.api.views.register import RegisterAPIList
from cloth_app.api.views.cart import CartAPIList,UserCheckAPIList
from cloth_app.api.views.admin_utility import AdminUtilityAPIList,AdminUtilityLoginAPIList
from cloth_app.api.views.wishlist import WishListAPIList
from cloth_app.api.views.first_page import FirstPageAPIList
from cloth_app.api.views.order import OrderApiView
from cloth_app.api.views.verify_otp import VerifyOtpAPIList
# from allauth.account.views import PasswordResetView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home', HomeAPIList.as_view() , name='home'),
    path('admin_utility', AdminUtilityAPIList.as_view() , name='admin_utility'),
    path('admin_utility_login', AdminUtilityLoginAPIList.as_view() , name='admin_utility_login'),
    path('login/', HomeAPIList.as_view() , name='login'),
    path('first_page/', FirstPageAPIList.as_view() , name='first_page'),
    path('categories/<str:gender>/', CategoryAPIList.as_view() , name='categories'),
    path('product_api/', ProductAPIList.as_view() , name='product_api'),
    path('product_detail_api/',AllProductAPIList.as_view(), name='product_detail_api'),
    path('register', RegisterAPIList.as_view() , name='register'),
    path('wishlist', WishListAPIList.as_view() , name='wishlist'),
    path('register/<int:variant>', RegisterAPIList.as_view() , name='register_variant'),
    path('order', OrderApiView.as_view() , name='order'),
    path('check_user', UserCheckAPIList.as_view() , name='check_user'),
    path('cart', CartAPIList.as_view() , name='cart'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_utility_logout/', LogoutView.as_view(next_page='admin_utility_login'), name='admin_utility_logout'),
    path('verify_otp', VerifyOtpAPIList.as_view() , name='verify_otp'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='forgot_password.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_complete'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

