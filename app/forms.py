from django import forms

from .models import User

# class ProductForm(forms.ModelForm):
#     title       = forms.CharField(label='', 
#                     widget=forms.TextInput(attrs={"placeholder": "Your title"}))
#     description = forms.CharField(
#                         required=False, 
#                         widget=forms.Textarea(
#                                 attrs={
#                                     "placeholder": "Your description",
#                                     "class": "new-class-name two",
#                                     "id": "my-id-for-textarea",
#                                     "rows": 20,
#                                     'cols': 120
#                                 }
#                             )
#                         )
#     price       = forms.DecimalField(initial=199.99)
    
#     class Meta:
#         model = Product
#         fields = [
#             'title',
#             'description',
#             'price'
#         ]

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)


class SignupForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)
    name = forms.CharField(label='Name', max_length=100)
    contact = forms.CharField(label='Contact', max_length=10)
    email = forms.EmailField(label='Email', max_length=100)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'name',
            'contact',
            'email'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)  # Get the instance without saving yet
        instance.id = User.objects.count()  # Initialize missing fields
        instance.done = False  # Setting default value
        instance.rem_time = 7200  # Setting default value
        if commit:
            instance.save()
        return instance
