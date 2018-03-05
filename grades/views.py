from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return HttpResponse(
        '''<html>
                <head>
                    <title>Gradebook</title>
                </head>
                <body>
                </body>
            </html>'''
    ) 
