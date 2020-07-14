from django import forms
from allauth.account.forms import LoginForm
from django.forms import ModelForm
from core.models import RequiredProduct
from core.models import Order, Item, Choices, OrderItem
from allauth.account.forms import ChangePasswordForm


class RequiredProductForm(forms.ModelForm):

    class Meta:
        model = RequiredProduct
        fields = '__all__'


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': "firstName",
            'class': 'form-control'
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': "lastName",
            'class': 'form-control'
        }
    ))
    # username = forms.CharField(widget=)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'id': "email",
            'class': 'form-control',
            'placeholder': 'user@exapmle.com'
        }
    ))
    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': "address",
            'class': 'form-control',
            'placeholder': '1234 Main Street 1'
        }
    ))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1111',
        'class': 'form-control',
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'id': "address",
        'class': 'form-control',
        'placeholder': 'Your City'
    }))


class ChoicesForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['color', 'size']

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


class ChoicesForm(forms.ModelForm):

    class Meta:
        model = Choices
        fields = '__all__'


class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem

        fields = ['color', 'size', 'quantity']
