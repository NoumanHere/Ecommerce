from django import forms
from allauth.account.forms import LoginForm
from django.forms import ModelForm
from core.models import RequiredProduct


class RequiredProductForm(forms.ModelForm):

    class Meta:
        model = RequiredProduct
        fields = '__all__'
