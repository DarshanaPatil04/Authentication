from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from .models import Email
from .middlewares import auth, guest
from openpyxl import Workbook 
from django.contrib.auth.models import User
from xhtml2pdf import pisa
import logging
from .forms import CustomUserCreationForm
from twilio.rest import Client
from django.conf import settings
from django.http import JsonResponse
import json
import random
import string 
import http.client
import requests
from urllib.parse import urlencode
# Logger configuration
logger = logging.getLogger('django')

# Views

@guest
def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('dashboard')
    return render(request, 'auth/register.html', {'form': form})

@guest
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'auth/login.html', {'form': form})

@auth
def dashboard_view(request):
    print("Dashboard view was called!")  # Check your terminal
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')

def google_auth(request):
    google_oauth_url = "https://accounts.google.com/o/oauth2/auth"
    redirect_url = f"{google_oauth_url}?client_id=426308882643-68dp5ss46tgnaeilr11ru4ihupru9l81.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:8000/auth/google/callback/&response_type=code&scope=email profile"
    return redirect(redirect_url)

def google_callback(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('home')

# Export users to Excel
def export_users_to_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "User Data"

    # Add headers
    ws.append(['ID', 'Username', 'Email', 'Date Joined'])

    # Fetch user data
    users = User.objects.all()

    for user in users:
        date_joined_naive = user.date_joined.replace(tzinfo=None) if user.date_joined else None
        ws.append([user.id, user.username, user.email, date_joined_naive])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=users_data.xlsx'  # File name for the download
    wb.save(response)

    return response

def export_invoices_to_pdf(request):
    # Dummy invoice data
    invoices = [
        {"invoice_number": "INV1001", "customer_name": "Alice", "issue_date": "2024-01-15", "total_amount": 150.25, "paid_status": True},
        {"invoice_number": "INV1002", "customer_name": "Bob", "issue_date": "2024-01-16", "total_amount": 200.50, "paid_status": False},
        {"invoice_number": "INV1003", "customer_name": "Charlie", "issue_date": "2024-01-17", "total_amount": 320.75, "paid_status": True},
    ]

    context = {'invoices': invoices}
    html_content = render(request, 'invoice_pdf.html', context).content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoices.pdf"'
    
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response

#  mobile number verification

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            phone_number = data.get('phone_number')

            if not phone_number:
                return JsonResponse({'error': 'Phone number is required'}, status=400)
            otp = generate_otp()
            url = f"https://2factor.in/API/V1/{settings.FAC_API_KEY}/SMS/{phone_number}/{otp}/Your OTP is {otp}"
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            # Send SMS
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                request.session[f'otp_{phone_number}'] = otp
                return JsonResponse({'message': 'OTP sent successfully.'}, status=200)
            else:
                return JsonResponse({
                    'error': f"Failed to send SMS. Status: {response.status_code}, Response: {response.text}"
                }, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)


# Function to verify OTP
def verify_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            otp = data.get('otp')

            if not phone_number or not otp:
                return JsonResponse({'error': 'Phone number and OTP are required'}, status=400)
            saved_otp = request.session.get(f'otp_{phone_number}')
            print(f"Saved OTP: {saved_otp}")
            print(f"OTP to verify: {otp}")
            print(f"Phone number: {phone_number}")
            if saved_otp and str(saved_otp) == str(otp):
                del request.session[f'otp_{phone_number}']
                return JsonResponse({'success': 'OTP verified successfully.'})
            else:
                return JsonResponse({'error': 'Invalid OTP or OTP has expired.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)
