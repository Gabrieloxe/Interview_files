import time
import csv
import pandas as pd
from time import sleep
import os.path
from random import randint
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import selenium.common.exceptions as selexcept
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

url = "https://nickangtc.github.io/travel-demo/#/hotels"
# change to your local web driver
driver = webdriver.Chrome(r'C:/Users/user/Desktop/chromedriver/chromedriver_win32/chromedriver.exe')
driver.implicitly_wait(120)
driver.get(url)
driver.maximize_window()

cities_list = []
hotels_list = []
hotel_entry = []
output = []

try:
    driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[1]/div/input[2]').click()
     
     # Get the dropdown list of cities
    cities = driver.find_elements_by_xpath('/html/body/div[1]/div/div/form/div[1]/div/ul/li/a')
    for city in cities:
        cities_list.append(city.text)

    sleep(randint(2,3))

    

    # get a list of the hotels for each selected city
    for a_city in cities_list:
        # Click on the city input bar, cause only by clicking then it will have the dropdown
        city_input = driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[1]/div/input[2]')
        # Enter the city name into the search bar
        city_input.send_keys(a_city)
        # Have to press the enter key before going to click the search button
        city_input.send_keys(Keys.ENTER)

        sleep(randint(2,3))
        # Click on the search button
        driver.find_element_by_xpath('/html/body/div[1]/div/div/form/a').click()

        sleep(randint(2,3))
        # Get all the hotel links for that city and append them into a list called hotels list
        hotels = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/a')
        for hotel in hotels:
            hotels_list.append(hotel.get_attribute('href'))
        
        sleep(randint(2,3))
        # This is to click on the city input bar 
        driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[1]/div/input[2]').click()
        # Locate the city input bar again as the element will be stale if you performed an action
        city_remove = driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[1]/div/input[2]')
        # Remove the current city in the city input so the next city could be keyed in
        city_remove.clear()
        sleep(randint(2,3))

    print("hotels extraction ok")    

    # Get all the hotel variables that is needed
    for hotel in hotels_list:
        driver.get(hotel)
        #retrieve hotel ID from the URL
        hotel_id = hotel.strip("https://nickangtc.github.io/travel-demo/#/hotels/").split("?")[0]

        #get the image source
        hotel_img = driver.find_element_by_class_name('hotel-image').get_attribute('src')
        hotel_name = driver.find_element_by_tag_name('h1').text
        hotel_price = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/h3[1]/span').text
        
        #count the number of stars in the hotel by using the number of characters
        hotel_ratings = len(driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/table/tbody/tr[5]/td[2]/i'))
        
        hotel_address = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/table/tbody/tr[1]/td[2]').text
        hotel_city = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/table/tbody/tr[2]/td[2]').text
        hotel_neighbourhood = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/table/tbody/tr[3]/td[2]').text
        hotel_country = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/table/tbody/tr[4]/td[2]').text
        
        # prep one hotel entry and append to the output
        hotel_entry = [hotel_id,hotel_name,hotel_price,hotel_img,hotel,hotel_city,hotel_address,hotel_neighbourhood,hotel_country,hotel_ratings]
        output.append(hotel_entry)

        #reset the list for the next entry
        hotel_entry = []
        sleep(randint(2,3))

    print("ready to print to csv")    
    df = pd.DataFrame(output,columns = ['Id','Name','Price/Night','Img Url','Hotel Url','City','Address','Neighbourhood','Country','Ratings'])
    
    #print the output to a csv file
    df.to_csv("hotel.csv",encoding = 'utf-8-sig') # The utf-8-sig is to remove the weird weird encodings

except Exception as e:
    print(e)
finally:
    driver.quit()