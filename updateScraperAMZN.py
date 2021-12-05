#Scrapes Amazon website for data - 'Xbox Series X', 'Playstation 5' and '3080 Graphics Card'
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_url(product):
    #replace every space with a + in order to get a working url
    product = product.replace(' ', '+')

    #url when searching a product
    url = f"https://www.amazon.com/s?k={product}&ref=nb_sb_noss_1"

    return url

def get_item_name(product):
    #gets the h2 tag of the product
    tag = product.find('a', 'a-link-normal a-text-normal')
    
    #strip extra info in order to get the name(text)
    product_name = tag.text
    return product_name


def get_item_url(product):
    #gets the h2 tag of the product
    tag =  product.find('a', 'a-link-normal a-text-normal')

    #gets the url of a specific product
    url = 'https://www.amazon.com' + tag.get('href')

    return url


def get_item_price(product):
    try:
        #go to the span tag thats called a-price
        price1 = product.find('span', 'a-price')
        #use price1 because the price is under the tag a-price
        price2 = price1.find('span', 'a-offscreen').text
    except :
        price = "Not available"
        return price
    #get rid of symbols in order to put them in a csv file
    price = price2.replace('$', '')
    price = price.replace(',', '')
    return float(price)


def get_item_rating(product):
    #get the tag i and only get text
    try:
        rating = product.i.text
    except :
        rating = "no ratings"
        return rating
    return rating


def get_number_of_reviews(product):
    try:
        parent = product.find('div', 'a-row a-size-small')
        number_of_reviews = parent.find('span', 'a-size-base').text
    except:
        number_of_reviews = "no reviews"
        return number_of_reviews
    return number_of_reviews


def get_item_stock(product):
    #find the tag called a-size-base a-color-price to get the stock
    try:
        stock = product.find('span', 'a-size-base a-color-price').text
    except :
        stock = "out of stock"
    return stock

def get_img(product):
    img = product.find('img', 's-image')
    print(img)
    found = img.get('src')

    return found


def create_a_dataframe(csv_name, product_info):
    headers = ['ASIN', 'price', 'rating', 'number_of_reviews', 'stock', 'img','name','url']
    df = pd.DataFrame(np.array(product_info), columns= headers)
    #df.to_csv(csv_name + ".csv", index = False)
    return df

def scrape_amazon():
    #hides chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    #open a google chrome search engine
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    
    product_information = []
    searched_item = ['Xbox Series X', 'Playstation 5', '3060 Graphics Card', '3070 Graphics Card', '3080 Graphics Card', '3090 Graphics Card', 'Radeon RX 6900 XT', 'Radeon RX 6800 XT']
    for i in searched_item:
        url = get_url(i)
    
        #loads the url
        driver.get(url)

        #get page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        #number of items
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        #loop through each item to get info
        for item in results:
            record = [item.get('data-asin'), get_item_price(item), get_item_rating(item), get_number_of_reviews(item), get_item_stock(item), get_img(item), get_item_name(item), get_item_url(item)]
            product_information.append(record)

    #closes google chrome 
    driver.quit()
    print("Total items scraped: " + str(len(product_information)))

    #create a dataframe with the data collected
    return create_a_dataframe('amazon_update', product_information)

amazon_df = scrape_amazon()
#print(amazon_df)