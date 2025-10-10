from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    password1= forms.CharField(
        label="Password",
        strip= False,
        widget=forms.PasswordInput(attrs={'autocomplet':'new-passqord'})
    )
    password2= forms.CharField(
        label="Password confirmation",
        strip= False,
        widget=forms.PasswordInput(attrs={'autocomplet':'new-passqord'})
    )
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("password1","password2")

