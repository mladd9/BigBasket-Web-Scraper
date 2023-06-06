# Importing libraries
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import time
import os


# Setting up directories and opening relevant files
start_time = time.time()

# Set the current working directory
os.chdir(r"C:\Users\17788\OneDrive\Desktop\VH RA")

# Read the CSV file containing URLs and category data
url_df = pd.read_csv(r"C:\Users\17788\OneDrive\Desktop\VH RA\Nad\URL and Category Data.csv")

# Get the list of URLs from the DataFrame
url_list = list(url_df['url'])


# Setting up Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome(options=chrome_options)


def product_scraper(url):
    """
    Scrape product information from a given URL.
    :param url: The URL to scrape.
    :return: A list of product characteristics.
    """
    print("Processing URL:", url)
    
    # Open the URL using Selenium
    driver.get(url)
    
    # Wait a randomly determined amount of seconds before retrieving the data
    randomly_sleep = np.random.uniform(4, 6)
    time.sleep(randomly_sleep)
    
    # Retrieve the HTML code
    html = driver.execute_script("return document.documentElement.outerHTML")
    
    # Create a BeautifulSoup object from the HTML code
    soup = bs(html, 'html.parser')
    
    # Find all products that loaded up on the page in the HTML script (?)
    products = soup.find_all('div', {'qa': 'product'})
    
    # Iterate through each product
    products_list = []
    for product in products:
        brand_name = product.find('div', {'qa': 'product_name'}).find('h6').text
        
        # Find the EAN number
        product_id = product.find('div', {'qa': 'product_name'}).find('a').get('href')
        for i in product_id.split('/'):
            if i.isnumeric():
                EAN = int(i)
            else:
                pass
        
        product_name = product.find('div', {'qa': 'product_name'}).find('a').text
        quantity = product.find("span", {"data-bind": "label"}).text
        price = product.find("span", {"ng-bind": "vm.selectedProduct.sp.replace('.00', '')"}).text
        
        try:
            MRP = product.find("span", {"ng-bind": "vm.selectedProduct.mrp.replace('.00', '')"}).text
        except:
            MRP = price
        
        product_char = [url, brand_name, EAN, product_name, quantity, price, MRP]
        products_list.append(product_char)
    
    return products_list


processed_urls = []
for i in url_list:
    output = product_scraper(i)
    processed_urls.extend(output)

df1 = pd.DataFrame(processed_urls)
df2 = None

end_time = time.time()
elapsed_time = end_time - start_time

print(f"This code runs in {elapsed_time} seconds.")
