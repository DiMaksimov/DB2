from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.utils.datetime_safe import datetime
from .models import DB2User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(
        years=range(datetime.today().year-1, 1939, -1),
    ))

    class Meta:
        model = DB2User
        fields = ('email', 'date_of_birth', 'country', 'city')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(
        years=range(datetime.today().year-1, 1939, -1),
    ))

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'date_of_birth', 'country', 'city', 'activated', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('User does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Wrong password')
            if not user.activated:
                raise forms.ValidationError('User is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)
