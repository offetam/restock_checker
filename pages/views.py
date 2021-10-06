from django.shortcuts import render
from django.http import HttpResponse
from pages.models import BestBuy

# Create your views here.
def home_view(request):
    context ={}
    if(request.method == 'GET'): #checks if we can GET
        x = request.GET.get("product") #gets the product name if possible
        #print(x) #prints the product name the user enters (to check)
        if(x is not None): #checks if the values we're getting is not None
            all_enteries = BestBuy.objects.all().filter(Name__contains=x) #checks if any product name contains x
            context = {'all_enteries': all_enteries} #creates a dictionary with our enteries
            #print(all_enteries)
        else:
            all_enteries = BestBuy.objects.all() #just gets all products if there's no input
            context = {'all_enteries': all_enteries} #creates a dictionary with our enteries
        #for i in all_enteries: #prints each product
            #print(str(i.SKU) + " " + i.Name + " " + str(i.price) + " " + i.Status + " " + i.URL + " " + str(i.Reviews))
    return render(request, 'mainpage.html',context)