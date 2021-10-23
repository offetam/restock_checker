from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
import csv


# open chrome
chrome_options = Options()
#chrome_options.add_argument("--headless") #REMOVE COMMENTS FOR HEADLESS
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()

def extract_info(item):
    try:
        #get sku
        skutag = item.p.i
        sku = skutag.text.strip()
        sku = re.findall(r': (.*)',sku)[0]
    except AttributeError:
        return
    '''
    #find item name
    atag = item.h2.a
    title = atag.text.strip()
    '''
    try:
        #get price
        price = str(item.find_all("strong","your-price"))
        price = re.findall(r'">(.*)<',price)[0]
    except IndexError:
        return

    try:
        #get stock info
        stocktag = str(item.find_all("button", attrs={"type": "button"}))
        t_stock = re.findall(r'        (.*)',stocktag)[0]
        if t_stock == "Add to Cart":
            stock = "In Stock"
        else:
            stock = "Not in Stock"
    except IndexError:
        return

    '''
    #get product url
    url_tag = item.find("a","tappable-item")
    url = url_tag.get("href")
    '''
    #get review
    review_parent = item.find("div","reviews-wrap")
    review = float(review_parent.find("em").text)

    #get number of reviews
    review_num_parent = item.find("span","review-count")
    review_num = int(review_num_parent.find("span").text)

    result = [sku,price,stock,review,review_num]
    return result
    
records = []

#https://www.adorama.com/l/Computers/Computer-Components/Video-and-Graphics-Cards?startAt=0&sf=relevance&st=de&perPage=25&sel=Price-Range_-dollar-400-to-dollar-2500
url = "https://www.adorama.com/l/Computers/Computer-Components/Video-and-Graphics-Cards?startAt="
end = "&sf=relevance&st=de&perPage=25&sel=Price-Range_-dollar-400-to-dollar-2500"

#pagination
for i in range(0,100,25):
    new_url = url + str(i) +end
    driver.get(new_url)
   

    soup = BeautifulSoup(driver.page_source, 'html.parser')


    time.sleep(25)
    #get item
    results = soup.find_all("div", 'item')
    print(len(results))

    for item in results:
            record = extract_info(item)
            if record:
                records.append(extract_info(item))

    time.sleep(5)

for item in records:
        print(item)

print(len(records))
#75
#driver.close()


#REMOVE COMMENTS TO SAVE TO CSV
#save data to csv
with open('adorama_update.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Sku','Price','Stock','Review','Number_of_Reviews'])
    writer.writerows(records)

