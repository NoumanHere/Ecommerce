from django import forms
from allauth.account.forms import LoginForm
from django.forms import ModelForm
from core.models import RequiredProduct
from core.models import Order


class RequiredProductForm(forms.ModelForm):

    class Meta:
        model = RequiredProduct
        fields = '__all__'


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'any@gmail.com',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1244 Street '
    }))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1111'
    }))
    city = forms.CharField()
    zip_code = forms.CharField()


# class CheckoutForm(forms.ModelForm):

#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'email', 'address',
#                   'postal_code', 'city', 'zip_code']
