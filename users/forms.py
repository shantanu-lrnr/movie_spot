from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from .models import CustomUser,UserList
from django import forms
from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(label = "password",max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label = "password(confirm again)",max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model = CustomUser
        fields = ["username","email"]

        widgets = {
            "username": forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Username"}),
            "email": forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter your Email"}),
        }
        

class UserAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True,"class":"form-control"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password","class":"form-control"}),
    )

class CreateListForm(forms.ModelForm):
    class Meta:
        model = UserList
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control","placeholder":"Enter List Name"}),
        }