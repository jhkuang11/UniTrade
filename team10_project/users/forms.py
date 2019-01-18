from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    '''Sign up which imports UserCreationForm, a built-in Django function'''
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(widget=forms.PasswordInput(), max_length=20, label="Password", help_text='Make sure password contains at least 8 characters and is not entirely numeric.')
    terms_and_conditions = forms.BooleanField(initial=False, required=True)

    class Meta:
        model = User
        fields = ('email','username','password1', 'password2', )
        exclude = ('terms_and_conditions',)