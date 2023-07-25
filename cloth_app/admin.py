from django.contrib import admin
from .models import Categories,Product,ProductVariant
# Register your models here.


@admin.register(Categories)
class Categories_UtilityAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'category_img')
#
# @admin.register(Product)
# class Product_UtilityAdmin(admin.ModelAdmin):
#     list_display = ( 'name','category','description','price','images','variants')
#
# @admin.register(ProductVariant)
# class ProductVariant_UtilityAdmin(admin.ModelAdmin):
#     list_display = ('product','size_choices','size','color')



