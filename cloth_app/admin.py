from django.contrib import admin
from .models import Categories,Product,ProductVariant,ProductImage,Subcategory,Order
# Register your models here.

# admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(Subcategory)
admin.site.register(Order)


# @admin.register(Categories)
# class Categories_UtilityAdmin(admin.ModelAdmin):
#     list_display = ('categoryName', 'category_img')


class CategoriesAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'subcategories':
            # If editing an existing category, filter subcategories based on the current category.
            if request.resolver_match.view_name == 'admin:%s_%s_change' % (
                    self.model._meta.app_label,
                    self.model._meta.model_name,
            ):
                category_id = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = Subcategory.objects.filter(category_id=category_id)

            # If adding a new category, don't show any subcategories until the category is saved.
            else:
                kwargs['queryset'] = Subcategory.objects.none()

        return super().formfield_for_manytomany(db_field, request, **kwargs)


# Register the custom admin class for the Categories model.
admin.site.register(Categories, CategoriesAdmin)


# @admin.register(Product)
# class Product_UtilityAdmin(admin.ModelAdmin):
#     # list_display = ( 'name','category','description','price','images','variants')
#
# @admin.register(ProductVariant)
# class ProductVariant_UtilityAdmin(admin.ModelAdmin):
#     # list_display = ('product','size_choices','size','color')


# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 0
#
# class ProductVariantInline(admin.TabularInline):
#     model = ProductVariant
#     extra = 0
#
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ProductImageInline, ProductVariantInline]
#
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         if db_field.name == 'images':
#             # If editing an existing product, filter images based on the current product.
#             if request.resolver_match.view_name == 'admin:%s_%s_change' % (
#                     self.model._meta.app_label,
#                     self.model._meta.model_name,
#             ):
#                 product_id = request.resolver_match.kwargs['object_id']
#                 kwargs['queryset'] = ProductImage.objects.filter(product__id=product_id)
#
#             # If adding a new product, don't show any images until the product is saved.
#             else:
#                 kwargs['queryset'] = ProductImage.objects.none()
#
#         elif db_field.name == 'variants':
#             # If editing an existing product, filter variants based on the current product.
#             if request.resolver_match.view_name == 'admin:%s_%s_change' % (
#                     self.model._meta.app_label,
#                     self.model._meta.model_name,
#             ):
#                 product_id = request.resolver_match.kwargs['object_id']
#                 kwargs['queryset'] = ProductVariant.objects.filter(product__id=product_id)
#
#             # If adding a new product, don't show any variants until the product is saved.
#             else:
#                 kwargs['queryset'] = ProductVariant.objects.none()
#
#         return super().formfield_for_manytomany(db_field, request, **kwargs)
#
#     def get_image_preview(self, obj):
#         if obj.images.exists():
#             return obj.images.first().image.url
#         return "(No Image)"
#
#     get_image_preview.short_description = 'Image Preview'
#
#     list_display = ['name', 'get_image_preview']

admin.site.register(Product)


