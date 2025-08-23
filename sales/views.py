from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum ,Q
from .models import Customer, FertilizerSale
from .forms import CustomerSearchForm, FertilizerSaleForm, OldDataForm
import pytz
from collections import defaultdict
from datetime import datetime, time

def format_aadhar_display(aadhar):
    """Format aadhar for display: XXXX XXXX XXXX"""
    if len(aadhar) == 12:
        return f"{aadhar[:4]} {aadhar[4:8]} {aadhar[8:]}"
    return aadhar

def clean_aadhar(aadhar):
    """Remove spaces from aadhar for database storage"""
    return aadhar.replace(" ", "")

# def homepage(request):
#     search_form = CustomerSearchForm()
#     sale_form = FertilizerSaleForm()
#     customer_history = None
    
#     if request.method == 'POST':
#         # Check if it's a search request
#         if 'search' in request.POST:
#             search_form = CustomerSearchForm(request.POST)
#             if search_form.is_valid():
#                 aadhar_formatted = search_form.cleaned_data['aadhar_number']
#                 aadhar = clean_aadhar(aadhar_formatted)
                
#                 try:
#                     customer = Customer.objects.get(aadhar_number=aadhar)
#                     sales = FertilizerSale.objects.filter(customer=customer).order_by('-sale_date')
                    
#                     if sales.exists():
#                         # Group sales by date and time
#                         grouped_sales = defaultdict(list)
#                         for sale in sales:
#                             ist = pytz.timezone('Asia/Kolkata')
#                             sale_datetime = sale.sale_date.astimezone(ist)
#                             # Format: DD-MM-YYYY and 12-hour time
#                             date_key = sale_datetime.strftime('%d-%m-%Y')
#                             time_key = sale_datetime.strftime('%I:%M %p')
#                             key = f"{date_key}|{time_key}"
#                             grouped_sales[key].append({
#                                 'fertilizer': sale.fertilizer_type,
#                                 'quantity': sale.quantity
#                             })
                        
#                         customer_history = {
#                             'aadhar': format_aadhar_display(aadhar),
#                             'sales': dict(grouped_sales)
#                         }
#                     else:
#                         customer_history = {'aadhar': format_aadhar_display(aadhar), 'sales': None}
#                 except Customer.DoesNotExist:
#                     customer_history = {'aadhar': format_aadhar_display(aadhar), 'sales': None}
#                 sale_form = FertilizerSaleForm(initial={'aadhar_number': aadhar_formatted})
                
#         # Check if it's a sale request
#         elif 'record_sale' in request.POST:
#             sale_form = FertilizerSaleForm(request.POST)
#             if sale_form.is_valid():
#                 aadhar_formatted = sale_form.cleaned_data['aadhar_number']
#                 aadhar = clean_aadhar(aadhar_formatted)
                
#                 # Get or create customer
#                 customer, created = Customer.objects.get_or_create(
#                     aadhar_number=aadhar,
#                     defaults={
#                         'customer_name': sale_form.cleaned_data.get('customer_name', 'Not Available'),
#                         'village': sale_form.cleaned_data.get('village', 'Not Available')
#                     }
#                 )
                
#                 # Get current IST time
#                 ist = pytz.timezone('Asia/Kolkata')
#                 current_time = timezone.now().astimezone(ist)
                
#                 # Create sales records for each fertilizer
#                 sales_recorded = []
                
#                 if sale_form.cleaned_data.get('urea_quantity'):
#                     FertilizerSale.objects.create(
#                         customer=customer,
#                         fertilizer_type='UREA',
#                         quantity=sale_form.cleaned_data['urea_quantity'],
#                         sale_date=current_time
#                     )
#                     sales_recorded.append(f"UREA: {sale_form.cleaned_data['urea_quantity']} bags")
                
#                 if sale_form.cleaned_data.get('dap_quantity'):
#                     FertilizerSale.objects.create(
#                         customer=customer,
#                         fertilizer_type='DAP',
#                         quantity=sale_form.cleaned_data['dap_quantity'],
#                         sale_date=current_time
#                     )
#                     sales_recorded.append(f"DAP: {sale_form.cleaned_data['dap_quantity']} bags")
                
#                 if sale_form.cleaned_data.get('potash_quantity'):
#                     FertilizerSale.objects.create(
#                         customer=customer,
#                         fertilizer_type='POTASH',
#                         quantity=sale_form.cleaned_data['potash_quantity'],
#                         sale_date=current_time
#                     )
#                     sales_recorded.append(f"POTASH: {sale_form.cleaned_data['potash_quantity']} bags")
                
#                 if sale_form.cleaned_data.get('twenty_twenty_quantity'):
#                     FertilizerSale.objects.create(
#                         customer=customer,
#                         fertilizer_type='20-20',
#                         quantity=sale_form.cleaned_data['twenty_twenty_quantity'],
#                         sale_date=current_time
#                     )
#                     sales_recorded.append(f"20-20: {sale_form.cleaned_data['twenty_twenty_quantity']} bags")
                
#                 messages.success(
#                     request, 
#                     f"Sale recorded successfully for Aadhar {format_aadhar_display(aadhar)}: {', '.join(sales_recorded)}"
#                 )
                
#                 # Reset the form
#                 sale_form = FertilizerSaleForm()
    
#     context = {
#         'search_form': search_form,
#         'sale_form': sale_form,
#         'customer_history': customer_history,
#     }
    
#     return render(request, 'sales/homepage.html', context)

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
                            'name': customer.customer_name,
                            'village': customer.village,
                            'sales': dict(grouped_sales)
                        }
                    else:
                        customer_history = {
                            'aadhar': format_aadhar_display(aadhar),
                            'name': customer.customer_name,
                            'village': customer.village,
                            'sales': None
                        }
                except Customer.DoesNotExist:
                    customer_history = {
                        'aadhar': format_aadhar_display(aadhar),
                        'name': 'Not Available',
                        'village': 'Not Available',
                        'sales': None
                    }
                
                # Preserve aadhar in sale form after search
                sale_form = FertilizerSaleForm(initial={'aadhar_number': aadhar_formatted})
        
        # Check if it's a sale request
        elif 'record_sale' in request.POST:
            sale_form = FertilizerSaleForm(request.POST)
            if sale_form.is_valid():
                aadhar_formatted = sale_form.cleaned_data['aadhar_number']
                aadhar = clean_aadhar(aadhar_formatted)
                
                # Get or create customer with name and village
                customer, created = Customer.objects.get_or_create(
                    aadhar_number=aadhar,
                    defaults={
                        'customer_name': sale_form.cleaned_data.get('customer_name', 'Not Available'),
                        'village': sale_form.cleaned_data.get('village', 'Not Available')
                    }
                )
                
                # If customer exists but doesn't have name/village, update them
                if not created:
                    update_needed = False
                    if customer.customer_name in ['Not Available', '']:
                        customer.customer_name = sale_form.cleaned_data.get('customer_name', 'Not Available')
                        update_needed = True
                    if customer.village in ['Not Available', '']:
                        customer.village = sale_form.cleaned_data.get('village', 'Not Available')
                        update_needed = True
                    if update_needed:
                        customer.save()
                
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
                    f"Sale recorded successfully for {customer.customer_name} (Aadhar: {format_aadhar_display(aadhar)}) from {customer.village}: {', '.join(sales_recorded)}"
                )
                
                # Reset the form
                sale_form = FertilizerSaleForm()
    
    context = {
        'search_form': search_form,
        'sale_form': sale_form,
        'customer_history': customer_history,
    }
    
    return render(request, 'sales/homepage.html', context)



# def all_details(request):
#     search_query = request.GET.get('search', '')
    
#     # Get all sales
#     all_sales = FertilizerSale.objects.select_related('customer').order_by('-sale_date')
    
#     # Apply search filter if provided
#     if search_query:
#         all_sales = all_sales.filter(
#             Q(customer_aadhar_number_icontains=search_query) |
#             Q(fertilizer_type__icontains=search_query)
#         )
    
#     # Format sales data
#     formatted_sales = []
#     for sale in all_sales:
#         ist = pytz.timezone('Asia/Kolkata')
#         sale_datetime = sale.sale_date.astimezone(ist)
#         formatted_sales.append({
#             'aadhar': format_aadhar_display(sale.customer.aadhar_number),
#             'name': sale.customer.customer_name,
#             'village': sale.customer.village,
#             'date': sale_datetime.strftime('%d-%m-%Y'),
#             'time': sale_datetime.strftime('%I:%M %p'),
#             'fertilizer': sale.fertilizer_type,
#             'quantity': sale.quantity
#         })
    
#     # Analytics
#     # Total bags by fertilizer type
#     total_by_type = {}
#     for ftype, fname in FertilizerSale.FERTILIZER_CHOICES:
#         total = FertilizerSale.objects.filter(fertilizer_type=ftype).aggregate(
#             total=Sum   ('quantity'))['total'] or 0
#         total_by_type[fname] = total
    
#     # Customer with highest total bags
#     # from django.db.models import Sum
#     customer_totals = Customer.objects.annotate(
#         total_bags=Sum('sales__quantity')
#     ).filter(total_bags__gt=0).order_by('-total_bags')
    
#     top_customer = None
#     if customer_totals.exists():
#         top = customer_totals.first()
#         top_customer = {
#             'aadhar': format_aadhar_display(top.aadhar_number),
#             'total_bags': top.total_bags
#         }
    
#     context = {
#         'sales': formatted_sales,
#         'search_query': search_query,
#         'total_by_type': total_by_type,
#         'top_customer': top_customer,
#         'total_sales': len(formatted_sales)
#     }
    
#     return render(request, 'sales/all_details.html', context)


def all_details(request):
    search_query = request.GET.get('search', '')
    
    # Get all sales
    all_sales = FertilizerSale.objects.select_related('customer').order_by('-sale_date')
    
    # Apply search filter if provided
    if search_query:
        all_sales = all_sales.filter(
            Q(customer_aadhar_number_icontains=search_query) |
            Q(fertilizer_type__icontains=search_query) |
            Q(customer_customer_name_icontains=search_query) |
            Q(customer_village_icontains=search_query)
        )
    
    # Group sales by customer and timestamp
    grouped_sales_dict = defaultdict(lambda: {
        'aadhar': '',
        'name': '',
        'village': '',
        'date': '',
        'time': '',
        'fertilizers': []
    })
    
    for sale in all_sales:
        ist = pytz.timezone('Asia/Kolkata')
        sale_datetime = sale.sale_date.astimezone(ist)
        
        # Create a unique key for each transaction (customer + datetime rounded to minute)
        datetime_key = sale_datetime.strftime('%Y-%m-%d %H:%M')
        transaction_key = f"{sale.customer.aadhar_number}_{datetime_key}"
        
        # Update the grouped sale information
        grouped_sales_dict[transaction_key]['aadhar'] = format_aadhar_display(sale.customer.aadhar_number)
        grouped_sales_dict[transaction_key]['name'] = sale.customer.customer_name
        grouped_sales_dict[transaction_key]['village'] = sale.customer.village
        grouped_sales_dict[transaction_key]['date'] = sale_datetime.strftime('%d-%m-%Y')
        grouped_sales_dict[transaction_key]['time'] = sale_datetime.strftime('%I:%M %p')
        
        # Add fertilizer to the list
        grouped_sales_dict[transaction_key]['fertilizers'].append({
            'type': sale.fertilizer_type,
            'quantity': sale.quantity
        })
    
    # Convert to list for template
    formatted_sales = list(grouped_sales_dict.values())
    
    # Sort by date and time (most recent first)
    formatted_sales.sort(key=lambda x: (x['date'].split('-')[::-1], x['time']), reverse=True)
    
    # Analytics
    # Total bags by fertilizer type
    total_by_type = {}
    for ftype, fname in FertilizerSale.FERTILIZER_CHOICES:
        total = FertilizerSale.objects.filter(fertilizer_type=ftype).aggregate(
            total=Sum('quantity'))['total'] or 0
        total_by_type[fname] = total
    
    # Customer(s) with highest total bags
    customer_totals = Customer.objects.annotate(
        total_bags=Sum('sales__quantity')
    ).filter(total_bags__gt=0).order_by('-total_bags')
    
    top_customers = []
    if customer_totals.exists():
        max_bags = customer_totals.first().total_bags
        # Get all customers with the maximum number of bags
        for customer in customer_totals:
            if customer.total_bags == max_bags:
                top_customers.append({
                    'aadhar': format_aadhar_display(customer.aadhar_number),
                    'name': customer.customer_name,
                    'village': customer.village,
                    'total_bags': customer.total_bags
                })
            else:
                break  # Since it's ordered, we can break when we find a lower value
    
    context = {
        'sales': formatted_sales,
        'search_query': search_query,
        'total_by_type': total_by_type,
        'top_customers': top_customers,
        'total_sales': len(formatted_sales)  # This now shows number of transactions, not individual sales
    }
    
    return render(request, 'sales/all_details.html', context)


def enter_old_data(request):
    # Get the last used date from session
    last_date = request.session.get('last_old_data_date', None)
    
    initial_data = {}
    if last_date:
        initial_data['sale_date'] = last_date
    
    if request.method == 'POST':
        form = OldDataForm(request.POST)
        if form.is_valid():
            aadhar_formatted = form.cleaned_data['aadhar_number']
            aadhar = clean_aadhar(aadhar_formatted)
            
            # Get or create customer
            customer, created = Customer.objects.get_or_create(
                aadhar_number=aadhar,
                defaults={
                    'customer_name': form.cleaned_data['customer_name'],
                    'village': form.cleaned_data['village']
                }
            )
            
            # Update customer info if exists
            if not created:
                customer.customer_name = form.cleaned_data['customer_name']
                customer.village = form.cleaned_data['village']
                customer.save()
            
            # Prepare datetime
            sale_date = form.cleaned_data.get('sale_date')
            sale_time = form.cleaned_data.get('sale_time')
            
            if sale_date:
                # Save the date in session for next entry
                request.session['last_old_data_date'] = sale_date.strftime('%d-%m-%Y')
                
                if sale_time:
                    # Combine date and time
                    sale_datetime = datetime.combine(sale_date, sale_time)
                else:
                    # Use noon as default time if no time provided
                    sale_datetime = datetime.combine(sale_date, time(12, 0))
                
                # Convert to timezone-aware datetime
                ist = pytz.timezone('Asia/Kolkata')
                sale_datetime = ist.localize(sale_datetime)
            else:
                # Use current time if no date provided
                ist = pytz.timezone('Asia/Kolkata')
                sale_datetime = timezone.now().astimezone(ist)
            
            # Create sales records
            sales_recorded = []
            
            if form.cleaned_data.get('urea_quantity'):
                FertilizerSale.objects.create(
                    customer=customer,
                    fertilizer_type='UREA',
                    quantity=form.cleaned_data['urea_quantity'],
                    sale_date=sale_datetime
                )
                sales_recorded.append(f"UREA: {form.cleaned_data['urea_quantity']} bags")
            
            if form.cleaned_data.get('dap_quantity'):
                FertilizerSale.objects.create(
                    customer=customer,
                    fertilizer_type='DAP',
                    quantity=form.cleaned_data['dap_quantity'],
                    sale_date=sale_datetime
                )
                sales_recorded.append(f"DAP: {form.cleaned_data['dap_quantity']} bags")
            
            if form.cleaned_data.get('potash_quantity'):
                FertilizerSale.objects.create(
                    customer=customer,
                    fertilizer_type='POTASH',
                    quantity=form.cleaned_data['potash_quantity'],
                    sale_date=sale_datetime
                )
                sales_recorded.append(f"POTASH: {form.cleaned_data['potash_quantity']} bags")
            
            if form.cleaned_data.get('twenty_twenty_quantity'):
                FertilizerSale.objects.create(
                    customer=customer,
                    fertilizer_type='20-20',
                    quantity=form.cleaned_data['twenty_twenty_quantity'],
                    sale_date=sale_datetime
                )
                sales_recorded.append(f"20-20: {form.cleaned_data['twenty_twenty_quantity']} bags")
            
            messages.success(
                request,
                f"Old data recorded successfully for {customer.customer_name} "
                f"(Date: {sale_datetime.strftime('%d-%m-%Y %I:%M %p')}): {', '.join(sales_recorded)}"
            )
            
            # Create new form with preserved date
            initial_data = {'sale_date': form.cleaned_data.get('sale_date')}
            form = OldDataForm(initial=initial_data)
    else:
        form = OldDataForm(initial=initial_data)
    
    context = {
        'form': form,
    }
    
    return render(request, 'sales/enter_old_data.html', context)

