from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from Product import Product
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
LOGGER.setLevel(logging.ERROR)
logging.basicConfig(filename='logfile.log', level=logging.INFO) 
class Scraper:
    def scrape(self,url):
        # Set up Chrome WebDriver with headless option
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument("disable-logging")
        driver = webdriver.Chrome(options = options, service = Service(ChromeDriverManager().install()))
        web = url
        driver.get(web) # Opens to the provided URL
        driver.set_page_load_timeout(10) # Set page load timeout to 10 seconds
        product=[]
        items=[]
        try:
            # Wait for presence of all elements with the specified XPath
            items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
        except TimeoutException as e:
             # Handle timeout exception by refreshing the page and retrying
            print("Timeout exception, refreshing the page...")
            driver.refresh()
            items=wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
                
        if len(items)>0:
            for item in items:
                P=Product()  # Create a new Product instance
                #Extract information of title,ratings,price and img_url
                try:
                    name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
                    if name.text==None:
                        name = item.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')
                    P.title=name.text
                except NoSuchElementException as e:
                     logging.info("Title:Unable to locate element")
                try:   
                    ratings=item.find_element(By.XPATH, './/span[@class="a-size-base s-underline-text"]')
                    P.ratings=ratings.text
                except NoSuchElementException as e:
                    logging.info("Ratings:Unable to locate element")

                try:
                    price=item.find_element(By.XPATH, './/span[@class="a-color-base"]')
                    P.price=price.text
                except NoSuchElementException as e:
                    logging.info("Price:Unable to locate element")
                try:
                    img_url=item.find_element(By.TAG_NAME ,'img')
                    P.img_url=img_url.get_attribute('src')
                except NoSuchElementException as e:
                   logging.info("Img_url:Unable to locate element")
                product.append(P) # Append the populated Product instance to the list
        
        driver.quit() #Quit the driver
        return product
        

