from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, password_validation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

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


class MyChangeFormPassword(PasswordChangeForm):
    pass


class ValidateUsername(forms.Form):
    username = UsernameField(label='Email Address',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    def clean_username(self):
        validating_email = self.cleaned_data['username']
        try:
            user = User.objects.get(username = validating_email)
        except User.DoesNotExist:
            raise forms.ValidationError('This user is not valid')

        return validating_email


class ChangeForgetPasswordForm(forms.Form):
    """
        A form that lets a user change set their password without entering the old
        password
        """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user



