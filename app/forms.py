from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Participant



class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=100)
    first_name = forms.CharField(label='First_Name', max_length=100)
    last_name = forms.CharField(label='Last_Name', max_length=100)
    contact = forms.CharField(label='Contact', max_length=10)

    class Meta:
        model = Participant
        fields = [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'contact',
            'email'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)  
        instance.contact = self.cleaned_data["contact"]
        instance.done = False  
        instance.rem_time = 7200
        if commit:
            instance.save()
        return instance
