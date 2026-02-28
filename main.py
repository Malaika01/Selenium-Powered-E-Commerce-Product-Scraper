import query_reader
from scraper import Scraper
import time
import json
from datetime import datetime
from data_saver import save_to_file

queries = query_reader.read_query() #Fetches queries from user_queries.json
basic_url = 'https://www.amazon.com/s?k='
S = Scraper()

for q in queries: # Loop over all the queries in user_queries.json
    all_products = []
    filename = q + ".json" #Creates a file with the name of the query e-g if the query is for headphones, headphones.json is created
    for page in range(1, 21): # Loop over 20 pages
        url = basic_url + q + "&page=" + str(page) #Construct url with basix url,query and page no.
        print("-------------------Fetching data for products", q, "on page", page,"----------------------------")
        try:
            # Call scrape function from Scraper class. The function returns a list of Product objects. 
            # Each object contains information of a single product of a specifi query
            products = S.scrape(url) 
            for product in products:
                try:
                    if product.price and "$" in product.price:
                        price = product.price
                    else:
                        price = "N/A"

                    product_json = {
                        "updatetime": int(time.time()),
                        "date": datetime.now().isoformat(),
                        "title": product.title,
                        "ratings": product.ratings,
                        "price": price,
                        "img_url": product.img_url
                    }
                    all_products.append(product_json)
                except Exception as e:
                    print("Error occurred while processing product:", e)
        except Exception as e:
            print("Error occurred while scraping:", e)
        time.sleep(2)
    save_to_file(all_products,filename)# Saves data to file
