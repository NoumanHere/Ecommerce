from django.contrib import admin
from .models import Order, OrderItem, Item, RequiredProduct, Category, Billing_Address, Profile, OrderUpdate, Instructions
from django.utils.safestring import mark_safe
from django.urls import reverse


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']

    list_filter = ['ordered']


admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(RequiredProduct)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'price',
                    'discount_price', 'catagory', 'description', 'slug']
    readonly_fields = ('image_tag',)
    list_filter = ['price', 'catagory']
    list_editable = ['price', 'discount_price', 'description']

    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Item, ItemAdmin)


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('core:admin_order_pdf', args=[obj.order_id])))
    order_pdf.short_description = 'Invoice'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'user', 'ordered', order_pdf]
    list_filter = ['ordered']


admin.site.register(Order, OrderAdmin)

admin.site.register(Billing_Address)

admin.site.register(Profile)

admin.site.register(OrderUpdate)


admin.site.register(Instructions)
