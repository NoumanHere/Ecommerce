from django import template
from core.models import Order, OrderItem
from django.shortcuts import get_object_or_404
register = template.Library()


@register.filter
def cart_items_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    else:
        return 0


# @register.filter
# def check_item_for_cart(user):
#     if user.is_authenticated:
#         item = get_object_or_404(Item, slug=slug)
#         qs = OrderItem.objects.filter(user=user, ordered=False)
#         order = qs[0]
#         if order.items.filter(item__slug=item.slug).exists():
#             return True
#     else:
#         return False
