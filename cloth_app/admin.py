from django.contrib import messages,admin
from .models import Categories,Product,ProductVariant,ProductImage,Subcategory,Order
# Register your models here.

# admin.site.register(Product)
# admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(Subcategory)
admin.site.register(Order)




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


@admin.register(ProductVariant)
class ProductVariant_UtilityAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Check if the field values are repetitive
        if obj.size:
            if change:  # This indicates that we are updating an existing object
                existing_variant = ProductVariant.objects.filter(size=obj.size).exclude(pk=obj.pk).first()
                if existing_variant:
                    # Update the quantity of the existing variant
                    existing_variant.quantity += obj.quantity
                    existing_variant.save()
                    messages.success(request, f"Quantity for Size {obj.size} updated successfully.")
                else:
                    # Save the object since there's no existing variant with the same size
                    super().save_model(request, obj, form, change)
                    messages.success(request, "Object saved successfully.")
            else:
                # Creating a new object
                if ProductVariant.objects.filter(size=obj.size).exists():
                    messages.set_level(request, messages.ERROR)
                    messages.error(request, f"Size {obj.size} already exists.")
                else:
                    super().save_model(request, obj, form, change)
                    messages.success(request, "Object saved successfully.")

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVariantInline]

    def save_model(self, request, obj, form, change):
        # Check if the field values are repetitive
        if hasattr(obj , 'size') :
            if ProductVariant.objects.filter(size=obj.size).exists():
                # Display an error message and prevent saving the object
                messages.set_level(request, messages.ERROR)
                messages.error(request, str(obj.size) + "Size already exist.")
                # self.message_user(request,   str(obj.size) + "Size already exist.", level='ERROR')
            else:
                # Save the object
                super().save_model(request, obj, form, change)
                messages.success(request, "Object saved successfully.")


    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'images':
            # If editing an existing product, filter images based on the current product.
            if request.resolver_match.view_name == 'admin:%s_%s_change' % (
                    self.model._meta.app_label,
                    self.model._meta.model_name,
            ):
                product_id = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = ProductImage.objects.filter(product__id=product_id)

            # If adding a new product, don't show any images until the product is saved.
            else:
                kwargs['queryset'] = ProductImage.objects.none()

        elif db_field.name == 'variants':
            # If editing an existing product, filter variants based on the current product.
            if request.resolver_match.view_name == 'admin:%s_%s_change' % (
                    self.model._meta.app_label,
                    self.model._meta.model_name,
            ):
                product_id = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = ProductVariant.objects.filter(product__id=product_id)

            # If adding a new product, don't show any variants until the product is saved.
            else:
                kwargs['queryset'] = ProductVariant.objects.none()

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_image_preview(self, obj):
        if obj.images.exists():
            return obj.images.first().image.url
        return "(No Image)"

    get_image_preview.short_description = 'Image Preview'

    list_display = ['name', 'get_image_preview']

admin.site.register(Product,ProductAdmin)


