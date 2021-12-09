from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from pages.models import BestBuy, MicroCenter, Gamestop, BH, AD, Amazon
from pages.models import User
from pages.models import products
from pages.models import Notification
from hashlib import blake2b
from django.contrib import messages
from django.core.mail import send_mail

import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pandas as pd
import random

def landing(request):
    if 'email' not in request.session:
        request.session['email'] = ''
    if(request.GET.get("product") is not None):
        x = request.GET.get("product")
        x = x.replace(' ','+')
        return redirect('/home/?product='+x)
    return render(request,'display.html')

def about(request):
    if 'email' not in request.session:
        request.session['email'] = ''
    if(request.GET.get("product") is not None):
        x = request.GET.get("product")
        x = x.replace(' ','+')
        return redirect('/home/?product='+x)
    return render(request, 'about.html')


# Create your views here.
def home_view(request,p = None):
    context ={}
    if 'email' not in request.session:
        request.session['email'] = ''
    if(request.method == 'GET'): #checks if we can GET
        if(p is None):
            x = request.GET.get("product") #gets the product name if possible
        else:
            x = p
        #print(x) #prints the product name the user enters (to check)
        if(x is not None): #checks if the values we're getting is not None
            split_str = x.split(' ')
            all_enteries = products.objects.all()
            for i in split_str:
                all_enteries = all_enteries.filter(product__icontains=i) #checks if any product name contains x
            #context = {'all_enteries': all_enteries} #creates a dictionary with our enteries
            uids =[]
            for i in all_enteries:
                #print(i.UUID)
                uids.append(i.UUID)
            combin_bb = BestBuy.objects.none()
            combin_mc = MicroCenter.objects.none()
            combin_gs = Gamestop.objects.none()
            combin_bh = BH.objects.none()
            combin_ad = AD.objects.none()
            combin_amzn = Amazon.objects.none()
            #file = 'Trends.csv'
            #df = pd.read_csv(file)
            #print(df)
            #date = getDates(df)
            #graph_arr = []
            for i in uids:
                #indices_list = df[df['UUID']==i.strip('\r')].index.values[0]
                combin_bb = combin_bb | BestBuy.objects.all().filter(BestBuy_UUID=i)
                #combin_bb = combin_bb | all_bb.filter(BestBuy_UUID=i).exclude(BestBuy_SKU=0)
                combin_mc= combin_mc | MicroCenter.objects.all().filter(MicroCenter_UUID=i).exclude(MicroCenter_SKU=0)
                combin_gs= combin_gs | Gamestop.objects.all().filter(Gamestop_UUID=i)
                combin_bh= combin_bh | BH.objects.all().filter(BH_UUID=i).exclude(BH_SKU="")
                combin_ad= combin_ad | AD.objects.all().filter(AD_UUID=i).exclude(AD_SKU="")
                combin_amzn = combin_amzn | Amazon.objects.all().filter(Amazon_UUID=i).exclude(Amazon_SKU="")
                #stock = df.loc[indices_list].tolist()
                #name = stock[0]
                #stock.pop(0) #get rid of product name from the list
                #stock.pop(0) #get rid of uuid from the list
                #stock = fixStock(stock)
                #print(stock)
                #graph_arr.append(get_plot(date,stock,name))
                #print(i)
            #chart = graph_arr
            context = {'all_enteries' : all_enteries,
            'bb_product' : combin_bb,
            'mc_product' : combin_mc,
            'gs_product' : combin_gs,
            'bh_product' : combin_bh,
            'ad_product' : combin_ad,
            'amzn_product' : combin_amzn}

        else:
            all_enteries = products.objects.all() #just gets all products if there's no input
            combin_bb = BestBuy.objects.all()
            combin_mc = MicroCenter.objects.all()
            combin_gs = Gamestop.objects.all()
            combin_bh = BH.objects.all()
            combin_ad = AD.objects.all()
            combin_amzn = Amazon.objects.all()
            context = {'all_enteries' : all_enteries,
            'bb_product' : combin_bb,
            'mc_product' : combin_mc,
            'gs_product' : combin_gs,
            'bh_product' : combin_bh,
            'ad_product' : combin_ad,
            'amzn_product' : combin_amzn} #creates a dictionary with our enteries
        y = request.GET.getlist('id')
        temp_arr = ""
        for i in y:
            #print(i)
            pro = products.objects.values('product').filter(UUID__contains=i)
            #print(pro)
            for q in pro:
                temp_arr = temp_arr + q.get('product') + "\n "
            if(request.session['email']==''):
                return redirect('/login')
            elif(Notification.objects.all().filter(email=request.session['email'], product__in=pro).count()>0):
                break
            else:
                temp = Notification.objects.create(email=request.session['email'], product = pro)
        if(len(temp_arr) != 0):
            send_mail('Notification',
            'Hello '+request.session['email']+',\nThe following items to be notified on: \n'+ temp_arr + "\nThank you for signing up with Restock \nFrom,\nRestock Team",
            'restockcheck123@gmail.com',
            [request.session['email']],
            fail_silently=False)
        #email_notify('BestBuy',['452d2196-6dd2-4503-b4fd-bfa5c7a07e43'])
        #email_notify('Gamestop',['a6def6f3-ee36-4029-8b07-a72652435b6a'])
        #email_notify('Amazon',['52c5d4f1-e686-44ae-830f-bfa3ffbc4c41'])
        #email_notify('AD',['20e99032-c794-4abf-949a-414518796cc9'])
        #email_notify('BH',['07e82650-a7c6-462a-9172-f661363a4475'])
    return render(request, 'mainpage.html',context)

def login(request):
    if(request.method == 'POST'):
        login_email = request.POST.get("login_email") #get login_email
        login_pass = request.POST.get("login_pass") #get login_pass
        signup_email = request.POST.get("signup_email") #get signup_email
        signup_pass = request.POST.get("signup_pass") #get signup_pass
        verification = request.POST.get("verificationcode")
        if(login_email is not None and login_pass is not None):
            #print(blake2b(login_email.encode()).hexdigest())
            hash_login_mail = blake2b(login_email.encode()).hexdigest() #hash the user's login_email
            salt = 'il0v3m3n' #salt string
            saltedpass = login_pass+salt #concat login_pass with salt
            #print(blake2b(saltedpass.encode()).hexdigest()) #hashes password
            hash_login_pass = blake2b(saltedpass.encode()).hexdigest() #hash the new salted user password
            x = User.objects.all().filter(email=hash_login_mail,password=hash_login_pass) #checks if the user's email and password exists
            if( not x): #gives error message and redirect user back if failed
                #print("No such User")
                messages.error(request, "Invalid Inputs", extra_tags='login')
                return redirect('/login?fail')
            else:
                for i in x:
                    check_code = i.verificationCode
                    isver = i.verify
                    failcount = i.numTry
                if(isver!=1 and (verification == '' or not(verification.isnumeric()))):
                    failcount +=1
                    x.update(numTry=failcount)
                    if(failcount>=5):
                        newcode(x,login_email)
                        failcount = 0
                        x.update(numTry=0)
                        messages.error(request, "Error logging in...New code sent to email", extra_tags='login')
                    else:
                        messages.error(request, "Error logging in", extra_tags='login')
                    return redirect('/login?notverified')
                elif(isver!=1 and check_code!= int(verification or 0)):
                    failcount +=1
                    x.update(numTry=failcount)
                    if(failcount>=5):
                        messages.error(request, "Error logging in...New code sent to email", extra_tags='login')
                        newcode(x,login_email)
                        failcount = 0
                        x.update(numTry=0)
                    else:
                        messages.error(request, "Error logging in", extra_tags='login')
                    return redirect('/login?notverified')
                else:
                    x.update(verify=1)
                    request.session['email']=login_email
                    return redirect('/')
        elif(signup_email is not None and signup_pass is not None):
            #print(blake2b(signup_email.encode()).hexdigest())
            hash_sign_mail = blake2b(signup_email.encode()).hexdigest() #hash the user's signup_email
            salt = 'il0v3m3n' #salt string
            saltedpass = signup_pass+salt #concat signup_pass with salt
            #print(blake2b(saltedpass.encode()).hexdigest())
            hash_sign_pass = blake2b(saltedpass.encode()).hexdigest() #hash the new salted user password
            x = User.objects.all().filter(email=hash_sign_mail).count() #checks if there's already an account with the inputted email
            if(x ==0): # creates new User and gives success message to user
                verCode = random.randrange(100000,999999)
                #print(verCode)
                new_user = User(email=hash_sign_mail,password=hash_sign_pass,verificationCode=verCode)
                new_user.save()
                messages.success(request,"User successfully created! Please go verify your account", extra_tags="signup_success")
                send_mail('Welcome to Restock: Verification',
                'Hi ' + signup_email + ', \nThank you for signing up with Restock. We hope we will meet your product needs. \nThis is your Verification Number:'+'\n'+str(verCode)+'\nFrom, \nRestock Team',
                'restockcheck123@gmail.com',
                [signup_email],
                fail_silently=False)
                return redirect('/login?signup_success')
            else: #gives error message and redirects users back if there already exists a user
                messages.error(request, "User exists already", extra_tags='signup_fail')
                return redirect('/login?signup_fail')
    return render(request, 'login.html')

def signout(request):
    #print(request.session['email'])
    request.session['email']= '' #just changes the user that's currently using the page
    #print(request.session['email'])
    return landing(request)

def notification(request):
    if(request.session['email']==""):
        return redirect('/login')
    if(request.GET.get("product") is not None):
        x = request.GET.get("product")
        return home_view(request,x)
    if(request.method == 'GET'):
        remove_notify = request.GET.getlist('id')
        #print(remove_notify)
        for pro in remove_notify:
            Notification.objects.all().filter(email=request.session['email'], product=pro).delete()
    notify = Notification.objects.all().filter(email=request.session['email'])
    context = {}
    context = {'notify' : notify}
    return render(request, 'notification.html', context)

#possible email notification based on items in stock (up for changes; currently testing only BestBuy)
def email_notify(Storename, arr):
    for i in arr:
        #print(i)
        if(Storename=='BestBuy'):
            link = BestBuy.objects.all().filter(BestBuy_UUID__UUID__contains=i)
            for l in link:
                link_one = l.BestBuy_URL
                #print(link_one)
        elif(Storename=='Gamestop'):
            link = Gamestop.objects.all().filter(Gamestop_UUID__UUID__contains=i)
            for l in link:
                link_one = l.Gamestop_URL
                #print(link_one)
        elif(Storename=='Amazon'):
            link = Amazon.objects.all().filter(Amazon_UUID__UUID__contains=i)
            for l in link:
                link_one = l.Amazon_URL
                #print(link_one)
        elif(Storename=='AD'):
            link = AD.objects.all().filter(AD_UUID__UUID__contains=i)
            for l in link:
                link_one = l.AD_URL
                #print(link_one)
        elif(Storename=='BH'):
            link = BH.objects.all().filter(BH_UUID__UUID__contains=i)
            for l in link:
                link_one = l.BH_URL
                #print(link_one)
        #print(link)
        product_name_query = products.objects.values('product').filter(UUID__contains=i)
        for j in product_name_query:
            product_name = j.get('product')
            #print(product_name)
        user_want_to_be_notify = Notification.objects.values('email').filter(product=product_name)
        for k in user_want_to_be_notify:
            user_email = k.get('email')
            #print(user_email)
            send_mail('IN STOCK NOW',
            'Hi '+ user_email +', \nThe following product is now available: \n'+ product_name+'\nHere is the link to the product: \n'+link_one + '\nThanks you for choosing Restock. \nFrom, \nRestock Team',
            'restockcheck123@gmail.com',
            [user_email],
            fail_silently=False)
    return 0
def update(StoreName,arr):
    if(StoreName=='BestBuy'):
        for i in range(len(arr[0])):
            user_obj=BestBuy.objects.get(BestBuy_SKU=int(arr[1][i]))
            if arr[2][i]>0:
                user_obj.BestBuy_price=arr[2][i]

            if len(arr[3][i])>0:

                user_obj.BestBuy_Status=arr[3][i]
            user_obj.save()
    if(StoreName=='Micro'):
        for i in range(len(arr[0])):
            user_obj=MicroCenter.objects.get(MicroCenter_SKU=int(arr[1][i]))
            if arr[2][i]>0:
                user_obj.MicroCenter_Price=arr[2][i]
            user_obj.save()
    if(StoreName=='Amazon'):
        for i in range(len(arr[0])):
            user_obj=Amazon.objects.get(Amazon_SKU=str(arr[1][i]))
            if float(arr[2][i])>0:
                user_obj.Amazon_price=arr[2][i]
            if len(arr[3][i])>0:
                user_obj.Amazon_Status=arr[3][i]
            user_obj.save()
    if(StoreName=='Gamestop'):
        for i in range(len(arr[0])):
            user_obj=Gamestop.objects.get(GameStop_SKU=str(arr[1][i]))
            if arr[2][i]>0:
                user_obj.Gamestop_price=arr[2][i]
            if len(arr[3][i])>0:
                user_obj.Gamestop_Status=arr[3][i]
            user_obj.save()
    return 0
def addProduct():
    return 1
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y,name):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,8))
    plt.title(name)
    plt.plot(x,y)
    plt.xticks(rotation=20)
    plt.xlabel('Date')
    plt.ylabel('Availability')
    plt.tight_layout()
    graph = get_graph()
    return graph


def getDates(df):
    dates = []
    for x in df.columns:
        if x != 'UUID' and x != 'Product_Name':
            dates.append(x)
    return dates

def fixStock(info):
    for x in range(len(info)):
        if info[x] == -1:
            info[x] = "No Data"
        if info[x] == 0:
            info[x] = "Not in Stock"
        if info[x] == 1:
            info[x] = "In Stock"
    return info

def product_detail(request, UUID):
    if(request.GET.get("product") is not None):
        x = request.GET.get("product")
        return home_view(request,x)
    detail = get_object_or_404(products, UUID = UUID)
    file = 'Trends.csv'
    df = pd.read_csv(file)
    date = getDates(df)
    graph_arr = []
    indices_list = df[df['UUID']==UUID.strip('\r')].index.values[0]
    stock = df.loc[indices_list].tolist()
    name = stock[0]
    stock.pop(0) #get rid of product name from the list
    stock.pop(0) #get rid of uuid from the list
    stock = fixStock(stock)
    #print(stock)
    graph_arr.append(get_plot(date,stock,name))
    #print(i)
    chart = graph_arr

    bb = BestBuy.objects.none() | BestBuy.objects.all().filter(BestBuy_UUID = detail.UUID)
    mc= MicroCenter.objects.none() | MicroCenter.objects.all().filter(MicroCenter_UUID= detail.UUID).exclude(MicroCenter_SKU=0)
    gs= Gamestop.objects.none() | Gamestop.objects.all().filter(Gamestop_UUID= detail.UUID)
    bh= BH.objects.none() | BH.objects.all().filter(BH_UUID= detail.UUID).exclude(BH_SKU="")
    ad= AD.objects.none() | AD.objects.all().filter(AD_UUID= detail.UUID).exclude(AD_SKU="")
    amzn = Amazon.objects.none() | Amazon.objects.all().filter(Amazon_UUID= detail.UUID).exclude(Amazon_SKU="")

    context = {'bb':bb,'mc': mc,'gs':gs,'bh':bh,'ad':ad,'amzn':amzn,'chart':chart,'detail':detail}

    return render(request, 'details.html', context)

def newcode(x,email):
    verCode = random.randrange(100000,999999)
    send_mail('Restock: New Verification Code',
                'Hi ' + email + ', \nThis is your new Verification Number:'+'\n'+str(verCode)+'\nFrom, \nRestock Team',
                'restockcheck123@gmail.com',
                [email],
                fail_silently=False)
    x.update(verificationCode=verCode)
    return 0

