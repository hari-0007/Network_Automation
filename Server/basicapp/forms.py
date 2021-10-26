from django import forms
from django.contrib.auth.models import User
from .models import BasicappUserprofileinfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = BasicappUserprofileinfo
        fields = ('portfolio_site','profile_pic')


#from django import forms
from .models import newuserForm

class FormnewuserForm(forms.ModelForm):
    class Meta:
        model= newuserForm
        fields= ["username", "email", "contact", "userid"]





from .models import Client

class ClientForm(forms.ModelForm):
        class Meta:
                model = Client
                fields ="__all__"





