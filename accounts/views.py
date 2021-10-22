from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
# Create your views here.

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request , user)
            return redirect('home')
    return render(request,template_name='signup.html',context={'form':form})