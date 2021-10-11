import pandas as pd
import pandasql as psql
from fuzzywuzzy import fuzz


amazon_file = 'limited_3.csv'
gamestop_file = 'gamestop_info.csv'



amazon = pd.read_csv(amazon_file)
gamestop = pd.read_csv(gamestop_file)

#columns
#Product_ID,Product_Name,Product_Price,Product_link,Product_Stock gamestop
#Name,price,rating,number of reviews,stock,url amazon

#organized prodcuts by brand
def organized_by_brand(brand):
    files = []
    for x in range(len(brand)):
        normalize_file = brand[x]+'{}.csv'
        file = normalize_file.format(x)
        files.append(file)
        grab_brand = "SELECT Name AS Product_Name, price AS Product_Price, url AS Product_link, stock AS Product_Stock FROM amazon WHERE Name LIKE" + " '%" + brand[x] + "%'"
        brand_gpu = psql.sqldf(grab_brand)

        grab_EVGA_2 = "SELECT Product_Name, Product_Price, Product_link, Product_Stock FROM gamestop WHERE Product_Name LIKE" + " '%" + brand[x] + "%'"
        brand_gpu_2 = psql.sqldf(grab_EVGA_2)


        both = pd.concat([brand_gpu, brand_gpu_2])
        both.to_csv(file, index = False)

    return files

#Xbox Series X
#Xbox Series S Digital Edition
#PlayStation 5 Console
#PlayStation 5 Digital Edition Console
def fix_console_names(console_name):
    if console_name.__contains__('Xbox Series X'):
        console_name = 'Xbox Series X'
    if console_name.__contains__('Xbox Series S'):
        console_name = 'Xbox Series S Digital Edition'
    if console_name.__contains__('PS') and console_name.__contains__('Bundle') or console_name.__contains__('PlayStation') and console_name.__contains__('Bundle'):
        console_name = 'PlayStation 5 Bundle'
    if console_name.__contains__('PlayStation') and console_name.__contains__('Disk'):
        console_name = 'PlayStation 5 Console'
    
    return console_name

    

#cleans out csv files to get rid of unneccesary products
#use Xbox Series X and playstation 5
def cleanup_consoles(csv_file):
    clean = pd.read_csv(csv_file)

    for value in clean['Product_Price'].items():
        if(value[1] != 'Not available'):
            if(float(value[1]) < 499): 
                clean.drop(index = value[0], inplace = True)
    

    clean['Product_Name'] = clean['Product_Name'].apply(fix_console_names)
    
    clean.to_csv(csv_file, index = False)


    
#cleans evga['Product_Name']
def fix_names(names):
    index = names.find('Card') + 4
    names = names[0:index]
    names = names.replace('PCIe', 'PCI Express')

    return names

def fix_price(prices):
    prices = prices.replace('$', '')
    prices = prices.replace(',', '')

    return prices

#clean evga0.csv
def normalize(csv_file):
    clean = pd.read_csv(csv_file)
    if csv_file == 'Xbox5.csv' or csv_file == 'Playstation4.csv':
        cleanup_consoles(csv_file)
    else:
        clean['Product_Name'] = clean['Product_Name'].apply(fix_names)

    clean['Product_Price'] = clean['Product_Price'].apply(fix_price)

    for value in clean['Product_Price'].items():
        if(value[1] != 'Not available'):
            if(float(value[1]) < 499): 
                clean.drop(index = value[0], inplace = True)
    
    clean.to_csv(csv_file, index = False)
    


brands = ['EVGA', 'MSI', 'ROG', 'ASUS', 'Playstation', 'Xbox']
files = organized_by_brand(brands)
for file in files:
    normalize(file)

together = []
for file in files:
    df = pd.read_csv(file)
    together.append(df)

done = pd.concat(together)
done.to_csv('normalize_version3.csv', index = False)

