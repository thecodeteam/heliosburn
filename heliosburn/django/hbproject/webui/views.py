from django.shortcuts import render


def dashboard(request):
    return render(request, 'dashboard.html')


def session_manager(request):
    return render(request, 'sessions/manager.html')


def session_details(request):
    return render(request, 'sessions/manager.html')