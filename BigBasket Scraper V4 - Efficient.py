from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import time
import os
from multiprocessing import Pool
from datetime import datetime

today = datetime.today().date()
formatted_date = today.strftime("%Y-%m-%d")


# Setting up directories and opening relevant files
# Set the current working directory
os.chdir(r"C:\Users\17788\OneDrive\Desktop\VH RA\Nad")

# Read the CSV file containing URLs and category data
url_df = pd.read_csv(r"C:\Users\17788\OneDrive\Desktop\VH RA\Nad\URL and Category Data.csv")

# Get the list of URLs from the DataFrame
url_list = list(url_df['url'])

def product_scraper(url, city_name, date):
    """
    Scrape product information from a given URL.
    :param url: The URL to scrape.
    :return: A list of product characteristics.
    """
    print("Processing URL:", url)
    
    # Open the URL using Selenium
    driver.get(url)
    
    # Wait for the product links to load on the page
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.prod-view >a")))
    except:
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.prod-view >a")))
    
    # Retrieve the HTML code
    html = driver.execute_script("return document.documentElement.outerHTML")
    
    # Create a BeautifulSoup object from the HTML code
    soup = bs(html, 'html.parser')
    
    # Find all products that loaded up on the page in the HTML script (?)
    products = soup.select('div[qa="product"]')

    # Iterate through each product
    products_list = []
    for product in products:
        brand_name = product.select_one('div[qa="product_name"] h6').text
        
        # Find the EAN number
        product_id = product.select_one('div[qa="product_name"] a')['href']
        EAN = int(next(filter(str.isdigit, product_id.split('/'))))
        
        product_name = product.select_one('div[qa="product_name"] a').text
        quantity = product.select_one('span[data-bind="label"]').text
        price = product.select_one('span[ng-bind="vm.selectedProduct.sp.replace(\'.00\', \'\')"]').text
        
        try:
            MRP = product.select_one('span[ng-bind="vm.selectedProduct.mrp.replace(\'.00\', \'\')"]').text
        except:
            MRP = price
        
        product_char = [city_name, date, url, brand_name, EAN, product_name, quantity, price, MRP]
        products_list.append(product_char)
    
    return products_list

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless=new')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.bigbasket.com/")

city_name = 'Bangalore'

processed_urls = []
for i in url_list:
    start_time = time.time()
    output = product_scraper(i, city_name, formatted_date)
    processed_urls.append(output)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"This URL runs in {elapsed_time} seconds.")

flat_list = [item for sublist in processed_urls for item in sublist]
df1 = pd.DataFrame(flat_list, columns=['city', 'date', 'url', 'Brand', 'EAN', 'Name', 'Quantity', 'Price', 'MRP'])

urls_to_data = pd.merge(url_df, df1, how='outer', on='url')

file_name = city_name + '-' + formatted_date + '.csv'
urls_to_data.to_csv(file_name, index=False)