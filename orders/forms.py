from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from django.contrib.auth.models import User

from .models import OrderDetail,Profile
# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class OrderDetailForm(forms.ModelForm):

    class Meta:
        model = OrderDetail
        fields = ['stamp_type', 'size', 'font', 'color','allignment','rate','quantity','spcl_request','advance','delivery_date']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar','company','designation','phone','address']
