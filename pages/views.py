from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request):
    if(request.method == 'GET'): #checks if we can GET
        x = request.GET.get("product") #gets the product name if possible
        print(x) #prints the product name the user enters (to check)
    return render(request, 'mainpage.html')