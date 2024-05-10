from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='',
                                         widget=forms.TextInput(attrs={
                                             'placeholder': 'Full Name',
                                             'class': 'form-control'}),
                                         required=True)
    shipping_email = forms.CharField(label='',
                                     widget=forms.TextInput(attrs={
                                         'placeholder': 'Email address',
                                         'class': 'form-control'}),
                                     required=True)
    shipping_address1 = forms.CharField(label='',
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Address 1',
                                            'class': 'form-control'}),
                                        required=True)
    shipping_address2 = forms.CharField(label='',
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'Address 2',
                                            'class': 'form-control'}),
                                        required=False)
    shipping_city = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'City',
                                        'class': 'form-control'}),
                                    required=True)
    shipping_state = forms.CharField(label='',
                                     widget=forms.TextInput(attrs={
                                         'placeholder': 'State',
                                         'class': 'form-control'}),
                                     required=False)
    shipping_country = forms.CharField(label='',
                                       widget=forms.TextInput(attrs={
                                           'placeholder': 'Country',
                                           'class': 'form-control'}),
                                       required=True)
    shipping_zipcode = forms.CharField(label='',
                                       widget=forms.TextInput(attrs={
                                           'placeholder': 'ZIP Code',
                                           'class': 'form-control'}),
                                       required=False)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name',
                  'shipping_email',
                  'shipping_address1',
                  'shipping_address2',
                  'shipping_city',
                  'shipping_state',
                  'shipping_country',
                  'shipping_zipcode']
        exclude = ['user',]


class PaymentForm(forms.Form):
    """
    Form for creating a payment transaction, without saving any data on the web server, use Stripe to handle it later.
    """
    card_name = forms.CharField(label='',
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Name on card',
                                    'class': 'form-control'}),
                                required=True)
    card_number = forms.CharField(label='',
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'Card number',
                                      'class': 'form-control'}),
                                  required=True)
    card_expiration_date = forms.CharField(label='',
                                           widget=forms.TextInput(attrs={
                                               'placeholder': 'Expiration date',
                                               'class': 'form-control'}),
                                           required=True)
    card_cvv = forms.CharField(label='',
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'CVV',
                                   'class': 'form-control'}),
                               required=True)
    card_address1 = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Billing address 1',
                                        'class': 'form-control'}),
                                    required=True)
    card_address2 = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Billing address 2',
                                        'class': 'form-control'}),
                                    required=True)
    card_city = forms.CharField(label='',
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Billing city',
                                    'class': 'form-control'}),
                                required=True)
    card_state = forms.CharField(label='',
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Billing state',
                                     'class': 'form-control'}),
                                 required=True)
    card_ZIPCode = forms.CharField(label='',
                                   widget=forms.TextInput(attrs={
                                       'placeholder': 'Billing ZIPCode',
                                       'class': 'form-control'}),
                                   required=True)
    card_country = forms.CharField(label='',
                                   widget=forms.TextInput(attrs={
                                       'placeholder': 'Billing country',
                                       'class': 'form-control'}),
                                   required=True)
