from django.contrib import admin
from .models import Order, OrderItem, Item, RequiredProduct,Category

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(RequiredProduct)


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category,CategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
	list_display = ['title', 'price','discount_price','catagory','description']
	list_filter = ['price','catagory']
	list_editable = ['price', 'discount_price','description']
    # prepopulated_fields = {'slug': ('title',)}
admin.site.register(Item,ItemAdmin)