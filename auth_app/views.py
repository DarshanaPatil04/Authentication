from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from .models import Email
from .middlewares import auth, guest
from openpyxl import Workbook  # Correct import
from django.contrib.auth.models import User  # Use the built-in User model
import logging


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
    redirect_url = f"{google_oauth_url}?client_id=426308882643-68dp5ss46tgnaeilr11ru4ihupru9l81.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:8000/auth/google/login/callback/&response_type=code&scope=email profile"
    return redirect(redirect_url)

def google_callback(request):
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

