from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import CreateUserForm, UpdateUserForm, UpdateProfileForm, LoginForm, CreateRecordForm, UpdateRecordForm
from .models import Record

def home(request):
    return render(request, 'webapp/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created successfully!')
            return redirect('my-login')
    context = {'form': form}
    return render(request, 'webapp/register.html', context)

@login_required(login_url='my-login')
@transaction.atomic
def update_profile(request):
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Account updated successfully!')
            return redirect('dashboard')
    context = {'form': user_form, 'profile': profile_form}
    return render(request, 'webapp/update-profile.html', context)

def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {'form': form}
    return render(request, 'webapp/my-login.html', context)

@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request, 'webapp/dashboard.html', context)

@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Record created successfully!')
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'webapp/create-record.html', context)

@login_required(login_url='my-login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request,'Record updated successfully!')
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'webapp/update-record.html', context)

@login_required(login_url='my-login')
def view_record(request, pk):
    record = Record.objects.get(id=pk)
    context = {'record': record}
    return render(request, 'webapp/view-record.html', context)

@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request,'Record deleted successfully!')
    return redirect('dashboard')

def user_logout(request):
    auth.logout(request)
    messages.success(request,'User logged out successfully!')
    return redirect('my-login')