"""
    Collect product datas from category pages
"""

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException


import json
import time
import random


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
url_target = "https://www.feelunique.com/skin/sun-tan/after-sun"
#url_target = "https://www.feelunique.com/makeup/lips/lipstick?filter=fh_location=//c1/en_GB/categories%3C{c1_c1c6}/categories%3C{c1_c1c6_c1c6c11}/categories%3C{c1_c1c6_c1c6c11_c1c6c11c1}/!exclude_countries%3E{gb}/!site_exclude%3E{1}/!brand={a70}/!restricted=1/%26customer-country=FR%26site_id=1%26gender=female%26device=desktop%26site_area=department%26date_time=20220822T082342%26fh_view_size=40%26fh_suppress=campaigns%2Credirect%26fh_start_index=0%26fh_view_size=120"

def accept_cookies(driver):
    cookieButton = driver.find_element(By.ID,"notice-ok")
    time.sleep(random.uniform(1,5))
    cookieButton.click()

def init_url_dict():
    """Initializes the dictionary with the urls data.

    Returns:
        dict: Dictionary with the urls data.
    """

    url_dict = {
        'product_name':None,
        'product_rating':None,
        'product_rating_count':None,
        'product_price':None,
        'product_discount':None,
        'product_value':None,
        'product_options':None,
        'free_gift_included':None
    }

    return url_dict


def main():
    try:
        #set the driver
        #s = Service(PATH_DRIVER)
        driver = webdriver.Chrome(PATH_DRIVER, options=options)
        driver.get(url_target)

        #accept cookies
        accept_cookies(driver)
        print("[LOG] Cookies accepted.")

        print(PATH_URLS_NEW)

        time.sleep(random.uniform(5, 10))

        #Showing all products by clicking loading more button
        while True:
            try:
                load_more_reviews_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                    By.CLASS_NAME, "loadMoreButton")))
                driver.execute_script("arguments[0].scrollIntoView(true);", load_more_reviews_btn)
                driver.execute_script("arguments[0].click();", load_more_reviews_btn)
                print("[LOG] Click on show more products button.")
                time.sleep(random.uniform(1, 5))
                
            except TimeoutException:
                print("[LOG] There isn’t any more products to show.")
                break
            except KeyboardInterrupt:
                print("[LOG] The collect has been interrupted by the user.")
                break
            except:
                break
        
        #make list of dicts
        #print('1')
        urls_dicts = []
        counter = 1
            
        #collect each product data
        products = driver.find_elements(By.CLASS_NAME, "Product")
        for product in products:
            print("[LOG] Collecting data of product ", counter)
            url_dict = init_url_dict()

            try:
                url_dict['url'] = product.find_element(By.TAG_NAME,"a").get_attribute("href")
            except:
                pass

            try:
                url_dict['product_name'] = product.find_element(By.CLASS_NAME,"Product-summary").text
            except:
                pass
            
            try:
                url_dict['product_rating'] = str(product.find_element(By.CLASS_NAME,"Rating-average").get_attribute('innerText'))
            except:
                url_dict['product_rating'] = None
                pass

            try:
                url_dict['product_rating_count'] = str(product.find_element(By.CLASS_NAME, "Rating-count").get_attribute('innerText'))
            except:
                 url_dict['product_rating_count'] = None
                 pass

            try:
                prix = str(product.find_element(By.CLASS_NAME,"Price-integer").get_attribute('innerText')) + str(product.find_element(By.CLASS_NAME,"Price-decimal").get_attribute('innerText')) 
                url_dict['product_price'] = prix
            except:
                url_dict['product_price'] = None
                pass

            try:
                url_dict['product_discount'] = product.find_element(By.CLASS_NAME, "Product-discount").text
            except:
                url_dict['product_discount'] = None
                pass
            
            try:
                url_dict['product_value'] = product.find_element(By.CLASS_NAME, "Product-value").text
            except:
                url_dict['product_value'] = None
                pass
            
            try:
                url_dict['product_options'] = product.find_element(By.CLASS_NAME, "value").text
            except:
                url_dict['product_options'] = None
                pass
            
            try:
                url_dict['free_gift_included'] = product.find_element(By.CLASS_NAME, "Product-offer").text
            except:
                url_dict['free_gift_included'] = None
                pass
            
            urls_dicts.append(url_dict)
            print("[LOG] Product ", counter, " collected, moving on to next product.")
            counter += 1

        with open(os.path.join(
                PATH_URLS_NEW, 'urls_new.json'), 'w', encoding='utf-8') as file_to_dump:
            json.dump(urls_dicts, file_to_dump, indent=4, ensure_ascii=False)

    except Exception as e:
        print(e)
        pass

    #delete cookies and quit when done
    print("[LOG] Deleting cookies and quitting the program.")
    driver.delete_all_cookies()
    driver.quit()

if __name__ == "__main__":
    main()


