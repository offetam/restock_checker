import matplotlib.pyplot as plt
import pandas as pd
import pandasql as psql
import plotly.express as px

import datetime

lol = datetime.datetime.now()
todays_date = lol.strftime("%x")

#MSI NVIDIA GeForce RTX 3070 Gaming Z Trio 8GB GDDR6 PCIe 4.0 Graphics Card good
#input_product = 'MSI AMD Radeon RX 6600 XT Gaming X 8GB GDDR6 PCIe 4.0 Graphics Card'
vendors = ['BestBuy', 'Adorama', 'Amazon', 'BH', 'GameStop']

for vendor in vendors:
    #vendor csv
    if vendor == 'BestBuy':
        input_file = 'testingBest.csv'
        input_file_3 = 'doneBB.csv'
    if vendor == 'Adorama':
        input_file = 'testingAD.csv'
        input_file_3 = 'doneAD.csv'
    if vendor == 'Amazon':
        input_file = 'testingAMZN.csv'
        input_file_3 = 'doneAMZN.csv'
    if vendor == 'BH':
        input_file = 'testingBH.csv'
        input_file_3 = 'doneBH.csv'
    if vendor == 'GameStop':
        input_file = 'testingGame.csv'
        input_file_3 = 'doneGAME.csv'
    if vendor == 'Microcenter':
        input_file = 'testingMicro.csv'
        input_file_3 = 'Micro_stock_trends.csv'

    #all items in our database
    input_file_2 = 'allitems.csv'

    def names(names):
        al = []
        al.append(names)
        return al



    #have to change df and df3
    df = pd.read_csv(input_file)
    df2 = pd.read_csv(input_file_2)
    df3 = pd.read_csv(input_file_3)
    #df3 = df3.fillna("na")
    #print(df3)

    allnames = []
    allnames = df3["UUID"].apply(names)
    #print(allnames)
    for x in allnames:
        ##### gets the uuid from the table with all items
        only_product = "SELECT UUID FROM df2 WHERE UUID =  " + "'" + x[0] + "'"
        uuid_product = psql.sqldf(only_product)

        first_value = uuid_product["UUID"][0] #get uuid
        #print(first_value)

        #from a vendor ###############################################################################

        if vendor == 'BestBuy':
            only_status = "SELECT BestBuy_Status FROM df WHERE UUID =  " + "'" + first_value + "'"
            status_product = psql.sqldf(only_status)
            #print(status_product)
            status_value = status_product['BestBuy_Status'][0]
        if vendor == 'Adorama':
            only_status = "SELECT Stock FROM df WHERE UUID =  " + "'" + first_value + "'"
            status_product = psql.sqldf(only_status)
            status_value = status_product['Stock'][0]
        if vendor == 'Amazon':
            only_status = "SELECT stock FROM df WHERE UUID =  " + "'" + first_value + "'"
            status_product = psql.sqldf(only_status)
            status_value = status_product['stock'][0]
        if vendor == 'BH':
            only_status = "SELECT Stock FROM df WHERE UUID =  " + "'" + first_value + "'"
            status_product = psql.sqldf(only_status)
            status_value = status_product['Stock'][0]
        if vendor == 'GameStop':
            only_status = "SELECT Product_Stock FROM df WHERE UUID =  " + "'" + first_value + "'"
            status_product = psql.sqldf(only_status)
            status_value = status_product['Product_Stock'][0]
        if vendor == 'Microcenter':
            only_status = "SELECT BestBuy_Status FROM df WHERE UUID =  " + "'" + first_value + "'"
            status_product = psql.sqldf(only_status)
            status_value = status_product['BestBuy_Status'][0]
        

        if status_value == 'ADD_TO_CART':
            status_value = 'In Stock'
        if status_value == 'Special Order' or status_value == 'Back-Ordered' or status_value == 'More on the Way' or status_value == 'Waiting List Only' or status_value == 'New Item - Coming Soon' or status_value == 'New Item - Special Order':
            status_value = 'Out of Stock'

        test = " SELECT * FROM df3 WHERE UUID = " + "'" + first_value + "'" 
        close = psql.sqldf(test)
        #print(close)

        #print(close.columns)
        date = []
        for x in close.columns:
            if x != 'UUID':
                date.append(x)

        first_date = date[0]
        

        ############################ GRABS THE INDEX ###########################
        index = df3.index
        condition = df3['UUID'] == first_value
        apple = index[condition]
        apples_indices_list = apple.tolist()
        #print(apples_indices_list[0])


        ########################## GETS THE STOCK ###############################
        stock = df3.loc[apples_indices_list[0]].tolist()
        stock.pop(0)
        #print(stock)

        ######################### UPDATE TRENDS ##################################
        if todays_date != todays_date:
            df3 = df3.drop(columns=first_date)
            df3[todays_date] = 'na'
        df3 = df3.fillna("na")

        ########################## update date and stock list ####################

        if date[7] != todays_date:
            date.append(todays_date)
            stock.append(status_value)
            #print(date)
            ########################### remove old date and statues ##################
            date.pop(0)
            stock.pop(0)

        ########################## update product ###############################
        df3.loc[apples_indices_list[0], todays_date] = status_value
      
        df3.to_csv(input_file_3,index=False)
