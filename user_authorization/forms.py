from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    address = forms.CharField(max_length=255, required=True, label='Address')
    house_number = forms.CharField(max_length=10, required=True, label='House Number')
    city = forms.CharField(max_length=100, required=True, label='City')
    postal_code = forms.CharField(max_length=10, required=True, label='Postal Code')

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'house_number', 'city', 'postal_code', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        username_lower = username.lower()
        if User.objects.filter(username__iexact=username_lower).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
