from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import html5lib
import time

start_time = time.time()

os.chdir(r"C:\Users\17788\OneDrive\Desktop\VH RA\Nad")  # Either comment this out or change to directory of interest

# Using Selenium to perform the HTTP Request because bigbasket blocks `requests`
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome(options=chrome_options)

# Navigating to the `All-Categories` URL
all_categories_url = "https://www.bigbasket.com/product/all-categories/"
driver.get(all_categories_url)

# Finding category/sub-category links, information, and URLs
r = driver.page_source
soup = bs(r, 'html5lib')
raw_links = soup.find_all('a')


def category_url_splice(raw_link):
    # This function goes through the HTML elements (?) to construct URLs and identify categories/subcategories (which are used later on)
    url = raw_link.get('href')
    if '/pc/' in url:
        cluster_info = list(filter(lambda item: item != '', url.split('/')))
        cluster_info[0] = "https://www.bigbasket.com" + url
        if '?nc' in cluster_info[-1]:
            # Sometimes the URL contained `?nc=bt` at the end. This is to remove that.
            cluster_info = cluster_info[:-1]
        if len(cluster_info) == 3:
            return None
        return cluster_info
    else:
        return None


processed_links = list(map(category_url_splice, raw_links))
# Removing `None` type items in the list
processed_links = list(filter(lambda item: item is not None, processed_links))
# Maps the `category_url_splice` function to each item in the `bs4.element.ResultSet` object.

# Converting the `processed_links` object, which will contain the URL, the main (top-level) category, a secondary category, and product-level category information into a DataFrame

col_names = ['url', 'primary_category', 'secondary_category', 'product_category']

url_category_df = pd.DataFrame(processed_links, columns=col_names)
# Saving the URL-Category DataFrame as a CSV file
url_category_df.to_csv('URL and Category Data.csv', index=False)

end_time = time.time()

elapsed_time = end_time - start_time

print(f"This code runs in {elapsed_time} seconds.")