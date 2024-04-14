from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User

from .models import Profile


class UserInfoForm(forms.ModelForm):
    phone_number = forms.CharField(label='', 
                                   widget=forms.TextInput(
                                       attrs={
                                           'placeholder': 'Phone number',
                                           'class': 'form-control'
                                       }
                                   ),
                                   required=False)
    address_one = forms.CharField(label='', 
                                   widget=forms.TextInput(
                                       attrs={
                                           'placeholder': 'Address 1',
                                           'class': 'form-control'
                                       }
                                   ),
                                   required=False)
    address_two = forms.CharField(label='', 
                                   widget=forms.TextInput(
                                       attrs={
                                           'placeholder': 'Address 2',
                                           'class': 'form-control'
                                       }
                                   ),
                                   required=False)
    city = forms.CharField(label='', 
                                   widget=forms.TextInput(
                                       attrs={
                                           'placeholder': 'City',
                                           'class': 'form-control'
                                       }
                                   ),
                                   required=False)
    state = forms.CharField(label='', 
                                   widget=forms.TextInput(
                                       attrs={
                                           'placeholder': 'State',
                                           'class': 'form-control'
                                       }
                                   ),
                                   required=False)
    zipcode = forms.CharField(label='', 
                                   widget=forms.TextInput(
                                       attrs={
                                           'placeholder': 'ZIP Code',
                                           'class': 'form-control'
                                       }
                                   ),
                                   required=False)
    country = forms.CharField(label='', 
                                   widget=forms.TextInput(
                                       attrs={
                                           'placeholder': 'Country',
                                           'class': 'form-control'
                                       }
                                   ),
                                   required=False)

    class Meta:
        model = Profile
        fields = ['phone_number', 'address_one', 'address_two', 'city', 'state', 'zipcode', 'country']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserInfoForm, self).__init__(*args, **kwargs)

    



class UpdateProfileForm(UserChangeForm):
    # hide password reset info
    password = None

    email = forms.EmailField(label='',
                             widget=forms.TextInput(
                                 attrs={
                                     'placeholder': 'Email address',
                                     'class': 'form-control'
                                 }
                             ),
                             required=False)
    first_name = forms.CharField(label='',
                                 max_length=100,
                                 widget=forms.TextInput(
                                     attrs={
                                         'placeholder': 'First name',
                                         'class': 'form-control'
                                    }
                                ),
                                required=False)
    last_name = forms.CharField(label='',
                                 max_length=100,
                                 widget=forms.TextInput(
                                     attrs={
                                         'placeholder': 'Last name',
                                         'class': 'form-control'
                                    }
                                ),
                                required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        # pass in bootstrap to override built in formatting
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'



class UpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

        # pass in bootstrap to override built in formatting
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='',
                             widget=forms.TextInput(
                                 attrs={
                                     'placeholder': 'Email address',
                                     'class': 'form-control'
                                 }
                             ))
    first_name = forms.CharField(label='',
                                 max_length=100,
                                 widget=forms.TextInput(
                                     attrs={
                                         'placeholder': 'First name',
                                         'class': 'form-control'
                                    }
                                ))
    last_name = forms.CharField(label='',
                                 max_length=100,
                                 widget=forms.TextInput(
                                     attrs={
                                         'placeholder': 'Last name',
                                         'class': 'form-control'
                                    }
                                ))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(SignUpForm, self).__init__(*args, **kwargs)

        # pass in bootstrap to override built in formatting
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
    