from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
import pytz

class Customer(models.Model):
    aadhar_validator = RegexValidator(
        regex=r'^\d{12}$',
        message='Aadhar number must be exactly 12 digits'
    )
    aadhar_number = models.CharField(
        max_length=12,
        validators=[aadhar_validator],
        unique=True
    )
    
    # In models.py, add these fields to the Customer class after aadhar_number:

    VILLAGE_CHOICES = [
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

    customer_name = models.CharField(
        max_length=100,
        default='Not Available',
        blank=True
    )
    village = models.CharField(
        max_length=50,
        choices=VILLAGE_CHOICES,
        default='Not Available',
        blank=True
    )

    # Update the _str_ method:
    def _str_(self):
        return f"{self.customer_name} - {self.aadhar_number} - {self.village}"
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return f"Customer: {self.aadhar_number}"

class FertilizerSale(models.Model):
    FERTILIZER_CHOICES = [
        ('UREA', 'UREA'),
        ('DAP', 'DAP'),
        ('POTASH', 'POTASH'),
        ('20-20', '20-20'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    fertilizer_type = models.CharField(max_length=10, choices=FERTILIZER_CHOICES)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of bags"
    )
    sale_date = models.DateTimeField()
    
    class Meta:
        ordering = ['-sale_date']
    
    def save(self, *args, **kwargs):
        if not self.sale_date:
            ist = pytz.timezone('Asia/Kolkata')
            self.sale_date = timezone.now().astimezone(ist)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.customer.aadhar_number} - {self.fertilizer_type} - {self.quantity}kg"