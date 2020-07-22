import django_filters
from core.models import Item
from django import forms


class ItemFilter(django_filters.FilterSet):
    # title = django_filters.ModelChoiceFilter(
    #     queryset=Item.objects.all(),
    #     widget=forms.Select(attrs={'ng-change': 'filterChanged()'}),
    #     empty_label="Any Item")
    price__lt = django_filters.NumberFilter(
        field_name='price', lookup_expr='gt', widget=forms.TextInput(attrs=(
            {
                'type': 'range',
                'name': 'price-min',
                'id': 'multi7',
                'min': 0,
                'max': 1000
            }
        )))
    price__gt = django_filters.NumberFilter(
        field_name='price', lookup_expr='lt', widget=forms.TextInput(attrs=(
            {
                'type': 'range',
                'name': 'price-max',
                'id': 'multi7',
                'min': 0,
                'max': 1000
            }
        )))

    class Meta:
        model = Item
        # form = FilterForm
        fields = ['catagory']


# class ItemFilter(django_filters.FilterSet):

#     title = django_filters.CharFilter(lookup_expr='icontains')
#     Category = django_filters.ChoiceFilter(
    # field_name='catagory', choices=PRICE_CHOICES)
    # price__gt = django_filters.NumberFilter(
    #     field_name='price', lookup_expr='gt')
    # price__lt = django_filters.NumberFilter(
    #     field_name='price', lookup_expr='lt')

    # class Meta:
    #     model = Item
    #     fields = {
    #         'price': ['lt', 'gt'],
    #     }
