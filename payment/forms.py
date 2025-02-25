from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
	shipping_full_name = forms.CharField(label="",
	                                     widget=forms.TextInput(
		                                     attrs={'class': 'form-control', 'placeholder': 'full-name'}),
	                                     required=True)
	shipping_email = forms.CharField(label="",
	                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
	                                 required=True)
	shipping_address1 = forms.CharField(label="",
	                                    widget=forms.TextInput(
		                                    attrs={'class': 'form-control', 'placeholder': 'address1'}),
	                                    required=True)
	shipping_address2 = forms.CharField(label="",
	                                    widget=forms.TextInput(
		                                    attrs={'class': 'form-control', 'placeholder': 'address2'}),
	                                    required=False)
	shipping_city = forms.CharField(label="",
	                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
	                                required=True)
	shipping_state = forms.CharField(label="",
	                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}),
	                                 required=True)
	shipping_zipcode = forms.CharField(label="",
	                                   widget=forms.TextInput(
		                                   attrs={'class': 'form-control', 'placeholder': 'zipcode'}),
	                                   required=True)
	shipping_country = forms.CharField(label="",
	                                   widget=forms.TextInput(
		                                   attrs={'class': 'form-control', 'placeholder': 'country'}),
	                                   required=True)

	class Meta:
		model = ShippingAddress
		fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city',
		          'shipping_state', 'shipping_zipcode', 'shipping_country']
		exclude = ['user', ]


class PaymentForm(forms.Form):
	card_name = forms.CharField(label="",
	                            widget=forms.TextInput(
		                            attrs={'class': 'form-control', 'placeholder': 'card_name'}),
	                            required=True)
	card_number = forms.CharField(label="",
	                              widget=forms.TextInput(
		                              attrs={'class': 'form-control', 'placeholder': 'card_number'}),
	                              required=True)
	card_exp_date = forms.CharField(label="",
	                                widget=forms.TextInput(
		                                attrs={'class': 'form-control', 'placeholder': 'card_exp_date'}),
	                                required=True)
	card_cvv_number = forms.CharField(label="",
	                                  widget=forms.TextInput(
		                                  attrs={'class': 'form-control', 'placeholder': 'card_cvv_number'}),
	                                  required=True)
	card_address1 = forms.CharField(label="",
	                                widget=forms.TextInput(
		                                attrs={'class': 'form-control', 'placeholder': 'card_address1'}),
	                                required=True)
	card_address2 = forms.CharField(label="",
	                                widget=forms.TextInput(
		                                attrs={'class': 'form-control', 'placeholder': 'card_address2'}),
	                                required=True)


