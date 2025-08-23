from django import forms
from django.core.validators import RegexValidator
from .models import FertilizerSale

VILLAGE_CHOICES = [
    ('', 'Select Village'),
    ('Dharmasagar', 'Dharmasagar'),
    ('Somadevarapalli', 'Somadevarapalli'),
    ('Devnoor', 'Devnoor'),
    ('Unikicherla', 'Unikicherla'),
    ('Elukurthy', 'Elukurthy'),
    ('Saipet', 'Saipet'),
    ('Kyathamapelli', 'Kyathamapelli'),
    ('Janakipuram', 'Janakipuram'),
    ('Velair', 'Velair'),
    ('Narayanagiri', 'Narayanagiri'),
    ('Peesara', 'Peesara'),
    ('Mallikudrla', 'Mallikudrla'),
    ('Shapalli', 'Shapalli'),
    ('Gundlasagaram', 'Gundlasagaram'),
    ('Peddapendyala', 'Peddapendyala'),
    ('Rampur', 'Rampur'),
    ('Dharmapur', 'Dharmapur'),
    ('Mallakapelli', 'Mallakapelli'),
    ('Ravigudem', 'Ravigudem'),
    ('Thatikayala', 'Thatikayala'),
]


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
    
        # In FertilizerSaleForm, add these fields after aadhar_number:

    customer_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Customer Name',
            'id': 'customer_name'
        })
    )

    village = forms.ChoiceField(
        choices=VILLAGE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'village'
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
    
    
class OldDataForm(forms.Form):
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
            'id': 'old_aadhar',
            'maxlength': '14'
        })
    )
    
    customer_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Customer Name'
        })
    )
    
    village = forms.ChoiceField(
        choices=VILLAGE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Date and Time fields (optional)
    sale_date = forms.DateField(
        required=False,
        input_formats= ['%d-%m-%Y', '%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'DD-MM-YYYY',
            'id': 'sale_date',
            'pattern': '[0-9]{2}-[0-9]{2}-[0-9]{4}'
        })
    )
    
    sale_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'id': 'sale_time'
        })
    )
    
    # Fertilizer quantities
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
        
        if not any([urea, dap, potash, twenty_twenty]):
            raise forms.ValidationError('Please select at least one fertilizer with quantity.')
        
        return cleaned_data