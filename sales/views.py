from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum ,Q
from .models import Customer, FertilizerSale
from .forms import CustomerSearchForm, FertilizerSaleForm
import pytz
from collections import defaultdict

def format_aadhar_display(aadhar):
    """Format aadhar for display: XXXX XXXX XXXX"""
    if len(aadhar) == 12:
        return f"{aadhar[:4]} {aadhar[4:8]} {aadhar[8:]}"
    return aadhar

def clean_aadhar(aadhar):
    """Remove spaces from aadhar for database storage"""
    return aadhar.replace(" ", "")

def homepage(request):
    search_form = CustomerSearchForm()
    sale_form = FertilizerSaleForm()
    customer_history = None
    
    if request.method == 'POST':
        # Check if it's a search request
        if 'search' in request.POST:
            search_form = CustomerSearchForm(request.POST)
            if search_form.is_valid():
                aadhar_formatted = search_form.cleaned_data['aadhar_number']
                aadhar = clean_aadhar(aadhar_formatted)
                
                try:
                    customer = Customer.objects.get(aadhar_number=aadhar)
                    sales = FertilizerSale.objects.filter(customer=customer).order_by('-sale_date')
                    
                    if sales.exists():
                        # Group sales by date and time
                        grouped_sales = defaultdict(list)
                        for sale in sales:
                            ist = pytz.timezone('Asia/Kolkata')
                            sale_datetime = sale.sale_date.astimezone(ist)
                            # Format: DD-MM-YYYY and 12-hour time
                            date_key = sale_datetime.strftime('%d-%m-%Y')
                            time_key = sale_datetime.strftime('%I:%M %p')
                            key = f"{date_key}|{time_key}"
                            grouped_sales[key].append({
                                'fertilizer': sale.fertilizer_type,
                                'quantity': sale.quantity
                            })
                        
                        customer_history = {
                            'aadhar': format_aadhar_display(aadhar),
                            'sales': dict(grouped_sales)
                        }
                    else:
                        customer_history = {'aadhar': format_aadhar_display(aadhar), 'sales': None}
                except Customer.DoesNotExist:
                    customer_history = {'aadhar': format_aadhar_display(aadhar), 'sales': None}
                sale_form = FertilizerSaleForm(initial={'aadhar_number': aadhar_formatted})
                
        # Check if it's a sale request
        elif 'record_sale' in request.POST:
            sale_form = FertilizerSaleForm(request.POST)
            if sale_form.is_valid():
                aadhar_formatted = sale_form.cleaned_data['aadhar_number']
                aadhar = clean_aadhar(aadhar_formatted)
                
                # Get or create customer
                customer, created = Customer.objects.get_or_create(aadhar_number=aadhar)
                
                # Get current IST time
                ist = pytz.timezone('Asia/Kolkata')
                current_time = timezone.now().astimezone(ist)
                
                # Create sales records for each fertilizer
                sales_recorded = []
                
                if sale_form.cleaned_data.get('urea_quantity'):
                    FertilizerSale.objects.create(
                        customer=customer,
                        fertilizer_type='UREA',
                        quantity=sale_form.cleaned_data['urea_quantity'],
                        sale_date=current_time
                    )
                    sales_recorded.append(f"UREA: {sale_form.cleaned_data['urea_quantity']} bags")
                
                if sale_form.cleaned_data.get('dap_quantity'):
                    FertilizerSale.objects.create(
                        customer=customer,
                        fertilizer_type='DAP',
                        quantity=sale_form.cleaned_data['dap_quantity'],
                        sale_date=current_time
                    )
                    sales_recorded.append(f"DAP: {sale_form.cleaned_data['dap_quantity']} bags")
                
                if sale_form.cleaned_data.get('potash_quantity'):
                    FertilizerSale.objects.create(
                        customer=customer,
                        fertilizer_type='POTASH',
                        quantity=sale_form.cleaned_data['potash_quantity'],
                        sale_date=current_time
                    )
                    sales_recorded.append(f"POTASH: {sale_form.cleaned_data['potash_quantity']} bags")
                
                if sale_form.cleaned_data.get('twenty_twenty_quantity'):
                    FertilizerSale.objects.create(
                        customer=customer,
                        fertilizer_type='20-20',
                        quantity=sale_form.cleaned_data['twenty_twenty_quantity'],
                        sale_date=current_time
                    )
                    sales_recorded.append(f"20-20: {sale_form.cleaned_data['twenty_twenty_quantity']} bags")
                
                messages.success(
                    request, 
                    f"Sale recorded successfully for Aadhar {format_aadhar_display(aadhar)}: {', '.join(sales_recorded)}"
                )
                
                # Reset the form
                sale_form = FertilizerSaleForm()
    
    context = {
        'search_form': search_form,
        'sale_form': sale_form,
        'customer_history': customer_history,
    }
    
    return render(request, 'sales/homepage.html', context)



def all_details(request):
    search_query = request.GET.get('search', '')
    
    # Get all sales
    all_sales = FertilizerSale.objects.select_related('customer').order_by('-sale_date')
    
    # Apply search filter if provided
    if search_query:
        all_sales = all_sales.filter(
            Q(customer_aadhar_number_icontains=search_query) |
            Q(fertilizer_type__icontains=search_query)
        )
    
    # Format sales data
    formatted_sales = []
    for sale in all_sales:
        ist = pytz.timezone('Asia/Kolkata')
        sale_datetime = sale.sale_date.astimezone(ist)
        formatted_sales.append({
            'aadhar': format_aadhar_display(sale.customer.aadhar_number),
            'date': sale_datetime.strftime('%d-%m-%Y'),
            'time': sale_datetime.strftime('%I:%M %p'),
            'fertilizer': sale.fertilizer_type,
            'quantity': sale.quantity
        })
    
    # Analytics
    # Total bags by fertilizer type
    total_by_type = {}
    for ftype, fname in FertilizerSale.FERTILIZER_CHOICES:
        total = FertilizerSale.objects.filter(fertilizer_type=ftype).aggregate(
            total=Sum   ('quantity'))['total'] or 0
        total_by_type[fname] = total
    
    # Customer with highest total bags
    # from django.db.models import Sum
    customer_totals = Customer.objects.annotate(
        total_bags=Sum('sales__quantity')
    ).filter(total_bags__gt=0).order_by('-total_bags')
    
    top_customer = None
    if customer_totals.exists():
        top = customer_totals.first()
        top_customer = {
            'aadhar': format_aadhar_display(top.aadhar_number),
            'total_bags': top.total_bags
        }
    
    context = {
        'sales': formatted_sales,
        'search_query': search_query,
        'total_by_type': total_by_type,
        'top_customer': top_customer,
        'total_sales': len(formatted_sales)
    }
    
    return render(request, 'sales/all_details.html', context)