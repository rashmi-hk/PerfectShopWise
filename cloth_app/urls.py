from django.urls import path
from cloth_app.api.views.home import HomeAPIList
from cloth_app.api.views.register import RegisterAPIList
from cloth_app.api.views.cart import CartAPIList
from cloth_app.api.views.verify_otp import VerifyOtpAPIList

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home', HomeAPIList.as_view() , name='home'),
    path('register', RegisterAPIList.as_view() , name='register'),
    path('cart', CartAPIList.as_view() , name='cart'),
    path('verify_otp', VerifyOtpAPIList.as_view() , name='verify_otp'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

