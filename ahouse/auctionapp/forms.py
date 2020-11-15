from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This email is already in use!")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


