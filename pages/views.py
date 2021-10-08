from django.shortcuts import render
from django.http import HttpResponse
from pages.models import BestBuy
from hashlib import blake2b

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

def login(request):
    if(request.method == 'POST'):
        login_email = request.POST.get("login_email")
        login_pass = request.POST.get("login_pass")
        signup_email = request.POST.get("signup_email")
        signup_pass = request.POST.get("signup_pass")
        if(login_email is not None and login_pass is not None):
            print(blake2b(login_email.encode()).hexdigest())
            print(blake2b(login_pass.encode()).hexdigest()) #hashes password
        elif(signup_email is not None and signup_pass is not None):
            print(blake2b(signup_email.encode()).hexdigest())
            print(blake2b(signup_pass.encode()).hexdigest())   
    return render(request, 'login.html')