from django import forms
from django.core.validators import RegexValidator
from .models import FertilizerSale

class CustomerSearchForm(forms.Form):
    aadhar_validator = RegexValidator(
        regex=r'^\d{4}\s\d{4}\s\d{4}$',
        message='Aadhar number must be in format: XXXX XXXX XXXX'
    )
    aadhar_number = forms.CharField(
        max_length=14,  # 12 digits + 2 spaces
        validators=[aadhar_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXXX XXXX XXXX',
            'id': 'search_aadhar',
            'maxlength': '14'
        })
    )

class FertilizerSaleForm(forms.Form):
    aadhar_number = forms.CharField(
        max_length=14,  # 12 digits + 2 spaces
        validators=[
            RegexValidator(
                regex=r'^\d{4}\s\d{4}\s\d{4}$',
                message='Aadhar number must be in format: XXXX XXXX XXXX'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXXX XXXX XXXX',
            'id': 'sale_aadhar',
            'maxlength': '14'
        })
    )
    
    # Fields for each fertilizer type - changed to IntegerField
    urea_quantity = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of bags',
            'min': '0'
        })
    )
    
    dap_quantity = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of bags',
            'min': '0'
        })
    )
    
    potash_quantity = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of bags',
            'min': '0'
        })
    )
    
    twenty_twenty_quantity = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of bags',
            'min': '0'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        urea = cleaned_data.get('urea_quantity')
        dap = cleaned_data.get('dap_quantity')
        potash = cleaned_data.get('potash_quantity')
        twenty_twenty = cleaned_data.get('twenty_twenty_quantity')
        
        # Check if at least one fertilizer is selected
        if not any([urea, dap, potash, twenty_twenty]):
            raise forms.ValidationError('Please select at least one fertilizer with quantity.')
        
        return cleaned_data