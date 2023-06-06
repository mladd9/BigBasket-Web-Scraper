from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import os
from datetime import datetime

global driver

today = datetime.today().date()
formatted_date = today.strftime("%Y-%m-%d")


# Setting up directories and opening relevant files
# Set the current working directory
os.chdir(r"C:\Users\17788\OneDrive\Desktop\VH RA\Nad")

# Read the CSV file containing URLs and category data
url_df = pd.read_csv(r"C:\Users\17788\OneDrive\Desktop\VH RA\Nad\URL and Category Data.csv")

# Get the list of URLs from the DataFrame
url_list = list(url_df['url'])

# List of cities that bigbasket operates in
city_list = ['Agra',
 'Ahmedabad Rural',
 'Ahmedabad-Gandhinagar',
 'Allahabad',
 'Amravati',
 'Amritsar',
 'Bangalore',
 'Bangalore Rural',
 'Bareilly',
 'Bhopal',
 'Bhopal Rural',
 'Bhubaneshwar-Cuttack',
 'Bhubaneswar Rural',
 'Chandigarh Rural',
 'Chandigarh Tricity',
 'Chennai',
 'Chennai Rural',
 'Coimbatore',
 'Coimbatore Rural',
 'Davanagere',
 'Delhi',
 'Gurgaon',
 'Gurugram Rural',
 'Guwahati',
 'Guwahati Rural',
 'Gwalior',
 'Hubli',
 'Hyderabad',
 'Hyderabad Rural',
 'Indore',
 'Indore Rural',
 'Jaipur',
 'Jaipur Rural',
 'Kochi',
 'Kochi Rural',
 'Kolkata',
 'Kolkata Rural',
 'Kozhikode',
 'Krishna District',
 'Lucknow Rural',
 'Lucknow-Kanpur',
 'Madurai',
 'Mumbai',
 'Mumbai Rural',
 'Mysore',
 'Mysore Rural',
 'Nagpur',
 'Nagpur Rural',
 'Nashik',
 'Nashik Business',
 'Noida Rural',
 'Noida-Ghaziabad',
 'Patna',
 'Patna Rural',
 'Pune',
 'Pune Rural',
 'Raipur',
 'Rajkot',
 'Ranchi',
 'Renigunta',
 'Surat',
 'Surat Rural',
 'Thiruvananthapuram',
 'Trichy',
 'Vadodara',
 'Vadodara Rural',
 'Vijayawada-Guntur',
 'Visakhapatnam',
 'Vizag Rural']

def product_scraper(url, city, formatted_date):
    """
    Scrape product information from a given URL.
    :param url: The URL to scrape.
    :return: A list of product characteristics.
    """
    print("Processing URL:", url)
    
    # A: Opening the category/sub-category level URL
    driver.get(url)
    
    # B: Waiting for the products to finish loading on the page by focusing on the text `That's all folks` that appears at the bottom of the page.
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//ul[last()]')))
    except:
        pass
    
    # C: Retrieving the HTML code for the loaded page
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = bs(html, 'html.parser')
    
    # Find all products that loaded up on the page in the HTML script (?)
    products = soup.select('div[qa="product"]')
    # E: For cities other than the default (Bangalore), the HTML becomes tricky. Previously, `products` was defined as `products = soup.select('div[qa="product"]')`. If this is an empty object, then the following code will run. This part of the code is for that complication.
    products_list = []
    if len(products) == 0:
        products_type_A = soup.select('li[class="PaginateItems___StyledLi-sc-1yrbjdr-0 dDBqny"]')
        for product in products_type_A:
            # 0: Skip if the product is unavailable
            try:
                available = product.select_one('button[class="Button-sc-1dr2sn8-0 CtaButtons___StyledButton2-sc-1tlmn1r-1 gJHNnE cxgxOd CtaOnDeck___StyledNotifyMeButton-sc-orwifk-8 gRhqfF CtaOnDeck___StyledNotifyMeButton-sc-orwifk-8 gRhqfF"]').text
                if available == 'Notify Me':
                    continue
            except:
                pass
            
            # i: Finding the brand name
            try:
                brand_name = product.select_one('span[class="Label-sc-15v1nk5-0 BrandName___StyledLabel2-sc-hssfrl-1 gJxZPQ keQNWn"]').text
            except:
                print("Brand name not found!")
                break
            
            # ii: Finding the EAN code
            try:
                product_id = product.select_one('a')['href']
                EAN = int(next(filter(str.isdigit, product_id.split('/'))))
            except:
                print("EAN ID not found!")
                break

            # iii: Finding the product name
            try:
                product_name = product.select_one('h3[class="block m-0 line-clamp-2 font-regular text-base leading-sm text-darkOnyx-800 pt-0.5 h-full"]').text
            except:
                print("Product name not found!")
                break

            # iv: Finding the quantity
            try:
                quantity = product.select_one('span[class="Label-sc-15v1nk5-0 PackChanger___StyledLabel-sc-newjpv-1 gJxZPQ cWbtUx"]').text
            except:
                quantity = product.select_one('span[class="Label-sc-15v1nk5-0 gJxZPQ truncate"]').text
            
            if len(quantity) == 0:
                print('No Quantity Found!')
                break
            
            # v: Finding the price (which may include a discount)
            try:
                price = product.select_one('span[class="Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ fcOOnE"]').text
            except:
                print("Price not found!")
                break
            price = price[1:]
            
            # vi: Finding the (non-discounted) price
            try:
                MRP = product.select_one('span[class="Label-sc-15v1nk5-0 Pricing___StyledLabel2-sc-pldi2d-2 gJxZPQ hsCgvu"]').text
                MRP = price[1:]
            except:
                MRP = price
                
            product_char = [city, formatted_date, url, brand_name, EAN, product_name, quantity, price, MRP] # Change the city_name and formatted_date part.
            products_list.append(product_char)
    return products_list


# Setting up Selenium
for city in city_list:
    city_start_time = time.time()
    print(city)
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless=new")
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    driver.get("https://www.bigbasket.com/")
    
    # Selecting the city
    # This button allows us to select a city
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="button"][value="Change Location"]')))
    button.click()
    print("Button clicked!")

    # This opens the dropdown menu
    dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.ui-select-toggle')))
    dropdown.click()
    print("Dropdown opened!")
    
    # This enters the city name (from the city list)
    textbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"][placeholder="Select your city"]')))
    textbox.clear()
    textbox.send_keys(city)
    textbox.send_keys(Keys.ENTER)
    print("City entered!")
    
    # Confirms chosen city
    button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[ng-click="vm.skipandexplore()"]')))
    button2.click()
    print("City confirmed!")
    
    time.sleep(5)

    processed_urls = []
    for i in url_list:
        start_time = time.time()
        output = product_scraper(i, city, formatted_date)
        processed_urls.append(output)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"This URL runs in {elapsed_time} seconds.")

    flat_list = [item for sublist in processed_urls for item in sublist]
    df1 = pd.DataFrame(flat_list, columns=['city', 'date', 'url', 'Brand', 'EAN', 'Name', 'Quantity', 'Price', 'MRP'])

    urls_to_data = pd.merge(url_df, df1, how='outer', on='url')

    file_name = city + '-' + formatted_date + '.csv'
    urls_to_data.to_csv(file_name, index=False)
    city_end_time = time.time()
    city_elapsed_time = city_start_time - city_end_time
    print(f"This city runs in {city_elapsed_time} seconds.")