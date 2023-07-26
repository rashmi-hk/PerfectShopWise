from django.urls import path
from cloth_app.api.views.home import HomeAPIList
from cloth_app.api.views.categories import CategoryAPIList
from cloth_app.api.views.product_api import ProductAPIList
from cloth_app.api.views.register import RegisterAPIList
from cloth_app.api.views.cart import CartAPIList
from cloth_app.api.views.verify_otp import VerifyOtpAPIList
# from allauth.account.views import PasswordResetView
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home', HomeAPIList.as_view() , name='home'),
    path('categories/<str:gender>/', CategoryAPIList.as_view() , name='categories'),
    path('product_api/', ProductAPIList.as_view() , name='product_api'),
    path('register', RegisterAPIList.as_view() , name='register'),
    path('cart', CartAPIList.as_view() , name='cart'),
    path('verify_otp', VerifyOtpAPIList.as_view() , name='verify_otp'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='forgot_password.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_complete'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

