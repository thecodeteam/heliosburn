from django.shortcuts import render


def signin(request):
    return render(request, 'signin.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def session_list(request):
    return render(request, 'sessions/list.html')


def session_details(request):
    return render(request, 'sessions/list.html')


def testplan_list(request):
    return render(request, 'testplan/list.html')


def testplan_details(request):
    return render(request, 'testplan/list.html')