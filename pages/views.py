from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request):
    x = request.GET #gets the request from the user
    print(x.__getitem__("product")) #prints the product name the user enters
    return render(request, 'mainpage.html')