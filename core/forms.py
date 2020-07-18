from django import forms
from allauth.account.forms import LoginForm
from django.forms import ModelForm
from core.models import RequiredProduct
from core.models import Order, Item, OrderItem
from allauth.account.forms import ChangePasswordForm


class RequiredProductForm(forms.ModelForm):

    class Meta:
        model = RequiredProduct
        fields = '__all__'
        exclude = ['email']


class CheckoutForm(forms.Form):
    # first_name = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         'id': "firstName",
    #         'class': 'form-control'
    #     }
    # ))
    # last_name = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         'id': "lastName",
    #         'class': 'form-control'
    #     }
    # ))
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': "fullname",
            'class': 'form-control',
            'placeholder': 'Username'
        }
    ))
    # email = forms.EmailField(widget=forms.EmailInput(
    #     attrs={
    #         'id': "email",
    #         'class': 'form-control',
    #         'placeholder': 'user@exapmle.com'
    #     }
    # ))
    phone_number = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'id': "phone_number",
            'class': 'form-control',
            'placeholder': 'e.g. +12125552368'
        }
    ))

    region = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': "region",
            'class': 'form-control',
            'placeholder': 'Region'
        }
    ))
    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': "address",
            'class': 'form-control',
            'placeholder': '1234 Main Street 1'
        }
    ))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'id': "address",
        'class': 'form-control',
        'placeholder': 'Your City'
    }))


# class ChoicesForm(forms.ModelForm):

#     class Meta:
#         model = Item
#         fields = ['color', 'size']

# class CheckoutForm(forms.ModelForm):

#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'email', 'address',
#                   'postal_code', 'city', 'zip_code']


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control mr-sm-2",
            'placeholder': "Search",
            'aria-label': "Search"
        }
    ))


class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem

        fields = ['color', 'size', 'quantity']


# class PanItemForm(forms.ModelForm):

#     class Meta:
#         model = OrderItem

#         fields = ['color', 'size', 'quantity', 'weight']
