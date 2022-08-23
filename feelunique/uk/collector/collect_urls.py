""" 
    Collect product datas from category pages
"""

import os
from tkinter.tix import COLUMN
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

import time
import random

import pandas as pd

#define paths
PATH_DRIVER = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
#os.path.join(os.curdir, 'chromedriver')
PATH_URLS_NEW = os.path.join(os.curdir, 'urls_new')

#set driver options to avoid getting detected as a bot
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

#define url
url_target = "https://www.feelunique.com/makeup/lips/lipstick?filter=fh_location=//c1/en_GB/categories%3C{c1_c1c6}/categories%3C{c1_c1c6_c1c6c11}/categories%3C{c1_c1c6_c1c6c11_c1c6c11c1}/!exclude_countries%3E{gb}/!site_exclude%3E{1}/!brand={a70}/!restricted=1/%26customer-country=FR%26site_id=1%26gender=female%26device=desktop%26site_area=department%26date_time=20220822T082342%26fh_view_size=40%26fh_suppress=campaigns%2Credirect%26fh_start_index=0%26fh_view_size=120"

def accept_cookies(driver):
    cookieButton = driver.find_element(By.ID,"notice-ok")
    time.sleep(random.uniform(1,5))
    cookieButton.click()

def check_if_load_more_exist(d, className):
    """ Checks if load more products button exist

    Args:
        d (Webdriver): Selenium WebDriver
        className (String): class name of the button

    Returns:
        Boolean
    """
    try :
        d.find_element(By.CLASS_NAME, className)
    except NoSuchElementException :
        print("[LOG] all products have been shown.")
        return False
    return True

def check_if_data_exist(d, className):
    """ Checks if a specific data (rating, discount, bonus, options, etc..) exists

    Args:
        d (Webdriver): Selenium WebDriver
        className (String): class name of the data

    Returns:
        Boolean
    """
    try:
        d.find_element(By.CLASS_NAME, className)
    except NoSuchElementException:
        print("[LOG] the data doesn't exist.")
        return False
    return True

def main():
    try:
        #set list of datas that are going to be scraped
        """
        Details: 
            product_url -> url string
            product_name -> string
            product_rating -> float (none if it doesn't have rating)
            product_rating_count -> int (none if it doesn't have rating)
            product_price -> float
            product_discount -> int (0 if it doesn't have one)
            free_gift_included -> boolean
            product_options -> int (shows how many options it has)
        """
        product_url = []
        product_name = [] 
        #product_rating = [] 
        #product_rating_count = []
        #product_price = [] 
        #product_discount = [] 
        #free_gift_included = [] 
        #product_options = []

        #print("[Log] begin surfing through products.")

        s = Service(PATH_DRIVER)
        #set the driver
        driver = webdriver.Chrome(service=s, options=options)
        driver.get(url_target)

        #accept cookies
        print("[Log] accepting cookies.")
        accept_cookies(driver)

        #show all products
        #counter = 1
        print("[LOG] Starting scrap.")
        load_more_exist = check_if_load_more_exist(driver, "loadMoreButton")
        while load_more_exist:
            try:
                #look for load more product button
                load_more_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "loadMoreButton"))
                )
                time.sleep(random.uniform(1,5))
                driver.execute_script('arguments[0].scrollIntoView(true);', load_more_btn)
                time.sleep(random.uniform(1,3))
                driver.execute_script('arguments[0].click();', load_more_btn)
                print("[LOG] Click on show more products button.")
                time.sleep(random.uniform(1,5))
                #load_more_exist = check_if_load_more_exist(driver, "loadMoreButton")
                #if not load_more_exist:
                #    print("[LOG] All products have been showed.")
                #    break
                    
            except:
                pass
        print("[LOG] All products have been showed.")

        #convert to json and save files  
        #print("[LOG] Converting and saving datas to JSON format")  
        #df = pd.DataFrame({"URL": product_url, "Product Name": product_name})
        # df.to_json("output.json", orient="records")
        # print("[LOG] JSON file saved in urls_new")

        """
        #collect each product datas
                    products = driver.find_elements(By.CLASS_NAME,"Product")
                    for product in products:
                        print("[LOG] Collecting datas of product " + counter +".")
                        tag_a = product.find_element(By.TAG_NAME,"a")
                        product_url.append(tag_a.get_attribute("href"))
                        product_name.append(product.find_element(By.CLASS_NAME,"Product-summary").text)
                        counter += 1
                        print("[LOG] Finished, moving to next product.")
                        #if check_if_data_exist(driver, "Rating"):
                        #    product_rating.append(str(product.find_element(By.CLASS_NAME,"Rating-average").get_attribute('innerHTML')))
                        #    product_rating_count.append(str(product.find_element(By.CLASS_NAME, "Rating-count").get_attribute('innerHTML')))
                        #else:
                            #    product_rating.append(None)
                            #    product_rating_count.append(None)
        """

    
    except:
        pass

    finally:
        #delete cookies and quit when done
        print("[LOG] Deleting cookies and quitting the program.")
        driver.delete_all_cookies()
        driver.quit()

if __name__ == "__main__":
    main()


