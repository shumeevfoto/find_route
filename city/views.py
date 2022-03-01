from django.shortcuts import render


def home(request):
    name = 'Dim'
    return render(request, 'home.html', {'name': name})

def about(request):
    return render(request, 'about.html')