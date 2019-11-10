from selenium import webdriver as sel
import requests
from bs4 import BeautifulSoup as bs
import json


def navigate(headers,base_url,url,product_list):

    #Initialising Connection Requests and HTML Parsing Homepage
    request = requests.get(url, headers = headers)
    soup = bs(request.text, "html.parser")

    #Finding The Woman Section Link
    woman_section = soup.find(attrs = {'class':'menu__super-link'}).get('href')
    #Requesting Woman Section Connection
    req_woman = requests.get(base_url+woman_section, headers = headers)
    #Parsing Woman Section HTML
    soup_woman = bs(req_woman.text, "html.parser")

    #Initialising Number of Items to be returned
    items = input("Enter the number of items to fetch: ")
    url_suffix = '?sort=stock&image-size=small&image=model&offset=0&page-size='+items

    #Finding Clothes Section
    clothes_section = soup_woman.find(attrs = {'class':'link','role':'menuitem'}).get('href')
    #Requesting Clothes Section Connection
    req_clothes = requests.get(base_url+clothes_section+url_suffix, headers = headers)
    #Parsing Clothes Section HTML
    soup_clothes = bs(req_clothes.text, "html.parser")

    #Obtaining List from all the products 
    results_set = list(soup_clothes.find_all(attrs = {'class':'link'}))
    product_list = [base_url+i.get('href') for i in results_set if 'productpage' in str(i)]

    
    fetch_description(product_list, headers)
    

def search_keyword(headers,base_url,product_list):

    #Initialisation
    keyword = input("Enter The Search Keyword: ")
    url_suffix = "&department=1&sort=stock&image-size=small&image=stillLife&offset=0&page-size="+input("Enter The Number of Items to fetch: ")
    url = "https://www2.hm.com/en_us/search-results.html?q="+keyword

    #Requesting Desired page connection and parsing its HTML
    request = requests.get(url+url_suffix, headers = headers)
    soup = bs(request.text, 'html.parser')

    #Looping through each product jjjnh
    for i in soup.find_all("a", class_= "link"):
        product_link = i.get("href")
        if "productpage" in product_link:
            product_list.append(base_url + product_link)

    fetch_description(product_list, headers)


def fetch_description(product_list, headers):
    
    #Visiting product URL for each product
    for i in product_list:
        request = requests.get(i , headers = headers)
        soup = bs(request.text, 'html.parser')

        #Converting Schema into a dictionary
        schema_data = soup.find('script', type = 'application/ld+json')
        schema_dict = json.loads(schema_data.text)

        prod_name = schema_dict['name']
        prod_color = schema_dict['color']
        prod_desc = schema_dict['description']


        #Retrieving Product Description using Schema
        print('\n\nProduct Name :',{prod_name},'\n\nProduct Color    :',{prod_color},'\n\nProduct Description    :',{prod_desc})


def main():

    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = "https://www2.hm.com"
    url = "https://www2.hm.com/en_us/index.html"
    product_list = []
    
    #navigate(headers,base_url,url,product_list)
    search_keyword(headers, base_url,product_list)

main()