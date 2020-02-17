from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()


def validateEmail(email):

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'first_name', 'last_name','password1', 'password2')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email Address'
        self.fields['first_name'].label = 'Display Name'
        self.fields['first_name'].required = True
        # Check out help_text for more

    def clean_username(self):
        current_email = self.cleaned_data['username']
        if validateEmail(current_email) == False:
            raise forms.ValidationError('Enter valid email')

        return current_email


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Email Address',
        widget=forms.TextInput(attrs={'autofocus': True})
    )