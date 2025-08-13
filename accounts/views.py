from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from .forms import LoginForm




def login_view(request):
    if request.user.is_authenticated:
        return redirect('/memberzone')

    if request.method == 'POST':
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/memberzone')
    return render(request, 'login.html', {'form': form})

# Create your views here.
