from django.shortcuts import render


def signin(request):
    return render(request, 'signin.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def session_manager(request):
    return render(request, 'sessions/manager.html')


def session_details(request):
    return render(request, 'sessions/manager.html')