import matplotlib.pyplot as plt
import pandas as pd
import pandasql as psql
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse


matplotlib.use("Agg")

input_file = 'Trends.csv'
df = pd.read_csv(input_file)

def getDates(df):
    dates = []
    for x in df.columns:
        if x != 'UUID' and x != 'Product_Name':
            dates.append(x)
    return dates

def getProductNames(df):
    names = []
    for x in range(len(df.index)):
        names.append(df.iloc[x, 0])
    return names

def fixStock(info):
    for x in range(len(info)):
        if info[x] == -1:
            info[x] = "No Data"
        if info[x] == 0:
            info[x] = "Not in Stock"
        if info[x] == 1:
            info[x] = "In Stock"
    return info

#django method           
def plot(request, name):
    input_file = 'Trends.csv'
    df = pd.read_csv(input_file)

    date = getDates(df)
    #Product_name = getProductNames(df)
    #Product_name = name

    #gets index based on Product_Name
    index = df.index
    #condition = df['Product_Name'] == Product_name[x]
    condition = df['Product_Name'] == name
    apple = index[condition]
    apples_indices_list = apple.tolist()

    #gets stock info based on product
    stock = df.loc[apples_indices_list[0]].tolist()
    stock.pop(0) #get rid of product name from the list
    stock.pop(0) #get rid of uuid from the list
    stock = fixStock(stock)

    fig, ax = plt.figure(figsize=(10, 8))
    ax.plot(date, stock)
    ax.title(name)
    ax.xlabel('Date')
    ax.ylabel('Stock Trend')
    ax.xticks(rotation=20)
    #ax.savefig("stock" + str(x) + ".png")
    #ax.close('all')

    response = HttpResponse(content_type = 'image/png')
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(response)
    return response

#2nd method
'''   
date = getDates(df)
Product_name = getProductNames(df)

total_product = len(df.index)
half = len(df.index)/2
#print(half)

for x in range(total_product):
    index = df.index
    condition = df['Product_Name'] == Product_name[x]
    apple = index[condition]
    apples_indices_list = apple.tolist()

    stock = df.loc[apples_indices_list[0]].tolist()
    stock.pop(0)
    stock.pop(0)
    stock = fixStock(stock)
    
    plt.figure(figsize=(10, 8))
    plt.plot(date, stock)
    plt.title(Product_name[x])
    plt.xlabel('date')
    plt.ylabel('stock trend')
    plt.xticks(rotation=20)
    plt.savefig("stock" + str(x) + ".png")
    plt.close('all')
'''
