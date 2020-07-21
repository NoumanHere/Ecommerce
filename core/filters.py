import django_filters
from core.models import Item

PRICE_CHOICES = (
    '250', '250',
    '300', '300'
)


class ItemsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(
        field_name='price', lookup_expr='gt',)
    price__lt = django_filters.NumberFilter(
        field_name='price', lookup_expr='lt')
