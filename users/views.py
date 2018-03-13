from django.shortcuts import render

# Create your views here.

def sign_up(request):
    if request.method == 'POST':
        return render(request, 'welcome.html')

    return render(request, 'sign_up.html')