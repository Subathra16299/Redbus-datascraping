from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
from datetime import datetime, timedelta
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.redbus.in/')

time.sleep(5)

from datetime import datetime, timedelta

# Function to convert time strings to datetime format
def convert_to_datetime(time_str, reference_date):
    try:
        dt = datetime.strptime(time_str, '%H:%M').replace(year=reference_date.year, month=reference_date.month, day=reference_date.day)
        return dt
    except ValueError:
        return None
    
# 10 states links for my reference
state_links = ["https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile"
               "https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile"
               "https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile"
               "https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile"
               "https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile"
               "https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile"
               "https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile"
               "https://www.redbus.in/online-booking/astc/?utm_source=rtchometile"
               "https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile"
               "https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile"
              ]
#open the browser

driver=webdriver.Chrome()

#load the webpage

driver.get("https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile")

time.sleep(3)

driver.maximize_window()

#retrive  bus links and route
wait = WebDriverWait(driver, 20)
def Kerala_link_route(path):   
    Links_Kerala=[]
    Route_Kerala=[]
    
    # retrive the route links 
    for i in range(1,3):
        paths=driver.find_elements(By.XPATH,path)
        
        for links in paths:
            d = links.get_attribute("href")
            Links_Kerala.append(d)
            
    # retrive names of the routes
        for route in paths:
            Route_Kerala.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_Kerala,Route_Kerala

Links_Kerala,Route_Kerala= Kerala_link_route("//a[@class='route']")

df_k=pd.DataFrame({"Route_name":Route_Kerala,"Route_link":Links_Kerala})
df_k

path=r"D:/Subathra/DataScience/Redbus/df_k.csv"
df_k.to_csv(path,index=False)

# read the csv file
df=pd.read_csv("df_k.csv")
df

#retrive the bus details
driver_k = webdriver.Chrome()
Bus_names_k = []
Bus_types_k = []
Start_Time_k = []
End_Time_k = []
Ratings_k = []
Total_Duration_k = []
Prices_k = []
Seats_Available_k = []
Route_names = []
Route_links = []

for i,r in df.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]

# Loop through each link
    driver_k.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_k.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2)
        
    # click elements to views bus
    try:
        clicks = driver_k.find_element(By.XPATH, "//div[@class='button']")
        clicks.click()
    except:
        continue  
    time.sleep(2)
    
    scrolling = True
    while scrolling:
        old_page_source = driver_k.page_source
        
        # Use ActionChains to perform a PAGE_DOWN
        ActionChains(driver_k).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver_k.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_k.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_k.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_k.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_k.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_k.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_k.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_k.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_k.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_k.append(bus.text)
        Route_links.append(link)
        Route_names.append(routes)
    for bus_type_elem in bus_type:  # elem--> elements
        Bus_types_k.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_k.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_k.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_k.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_k.append(ratings.text)
    for price_elem in price:
        Prices_k.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_k.append(seats_elem.text)
        
print("Successfully Completed")

# from list to convert data frame
data = {
    'Bus_name': Bus_names_k,
    'Bus_type': Bus_types_k,
    'Start_time': Start_Time_k,
    'End_time': End_Time_k,
    'Total_duration': Total_Duration_k,
    'Price': Prices_k,
    'Seats_Available':Seats_Available_k,
    'Ratings':Ratings_k,
    'Route_link': Route_links,
    'Route_name': Route_names
}

df_buses_1 = pd.DataFrame(data)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_1.csv" 
df_buses_1.to_csv(path,index=False)

df_buses_1

# Open the browser -- Andhra -- 2
driver_A = webdriver.Chrome()

# Load the webpage
driver_A.get("https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile")

time.sleep(3)

driver_A.maximize_window()

# Retrieve bus links and routes
wait = WebDriverWait(driver_A, 20)

def Andhra_link_route(path):   
    Links_Andhra = []
    Route_Andhra = []
    
    for i in range(1, 6):
        paths = driver_A.find_elements(By.XPATH, path)
        
        for links in paths:
            d = links.get_attribute("href")
            Links_Andhra.append(d)
            
        for route in paths:
            Route_Andhra.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver_A.execute_script("arguments[0].scrollIntoView();", next_button) 
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_Andhra, Route_Andhra

Links_Andhra, Route_Andhra = Andhra_link_route("//a[@class='route']")

df_A = pd.DataFrame({"Route_name": Route_Andhra, "Route_link": Links_Andhra})
df_A

path=r"D:/Subathra/DataScience/Redbus/df_A.csv"
df_A.to_csv(path,index=False)

# read the csv file
df_1=pd.read_csv("df_A.csv")
df_1

#retrive the bus details
driver_A = webdriver.Chrome()
Bus_names_A = []
Bus_types_A = []
Start_Time_A = []
End_Time_A = []
Ratings_A = []
Total_Duration_A = []
Prices_A = []
Seats_Available_A = []
Route_names = []
Route_links = []

for i,r in df_1.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]

# Loop through each link
    driver_A.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_A.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2)

    # click elements to views bus
    try:
        clicks = driver_A.find_element(By.XPATH, "//div[@class='button']")
        clicks.click()
    except:
        continue  
    time.sleep(2)
    
    scrolling = True
    while scrolling:
        old_page_source = driver_A.page_source
        
        # Use ActionChains to perform a PAGE_DOWN
        ActionChains(driver_A).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  # Adjust sleep time as needed
        
        new_page_source = driver_A.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_A.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_A.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_A.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_A.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_A.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_A.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_A.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_A.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_A.append(bus.text)
        Route_links.append(link)
        Route_names.append(routes)
    for bus_type_elem in bus_type:
        Bus_types_A.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_A.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_A.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_A.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_A.append(ratings.text)
    for price_elem in price:
        Prices_A.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_A.append(seats_elem.text)
        
print("Successfully Completed")

# from list to convert data frame
data_1 = {
    'Bus_name': Bus_names_A,
    'Bus_type': Bus_types_A,
    'Start_time': Start_Time_A,
    'End_time': End_Time_A,
    'Total_duration': Total_Duration_A,
    'Price': Prices_A,
    "Seats_Available":Seats_Available_A,
    "Ratings":Ratings_A,
    'Route_link': Route_links,
    'Route_name': Route_names
}

df_buses_2 = pd.DataFrame(data_1)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_2.csv"
df_buses_2.to_csv(path,index=False)

df_buses_2

# Open the browser -- Telungana -- 3

driver_T = webdriver.Chrome()

# Load the webpage
driver_T.get("https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile")

time.sleep(3)

driver_T.maximize_window()

# Retrieve bus links and routes
wait = WebDriverWait(driver_T, 20)

def Telugana_link_route(path):   
    Links_Telungana = []
    Route_Telungana = []
    
    for i in range(1, 4):
        paths = driver_T.find_elements(By.XPATH, path)
        
        # Retrieve the route links 
        for links in paths:
            d = links.get_attribute("href")
            Links_Telungana.append(d)
            
        # Retrieve names of the routes
        for route in paths:
            Route_Telungana.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver_T.execute_script("arguments[0].scrollIntoView();", next_button)  
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_Telungana, Route_Telungana

Links_Telungana, Route_Telungana = Telugana_link_route("//a[@class='route']")

df_T=pd.DataFrame({"Route_name":Route_Telungana,"Route_link":Links_Telungana})
df_T

path=r"D:/Subathra/DataScience/Redbus/df_T.csv"
df_T.to_csv(path,index=False)

# read the csv file
df_2=pd.read_csv("df_T.csv")
df_2

# retrive the bus details
driver_T = webdriver.Chrome()
Bus_names_T = []
Bus_types_T = []
Start_Time_T = []
End_Time_T = []
Ratings_T = []
Total_Duration_T = []
Prices_T = []
Seats_Available_T = []
Route_names = []
Route_links = []

for i,r in df_2.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]

# Loop through each link
    driver_T.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_T.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2)

    # click elements to views bus
    try:
        clicks = driver_T.find_element(By.XPATH, "//div[@class='button']")
        clicks.click()
    except:
        continue  
    time.sleep(2)
    
    scrolling = True
    while scrolling:
        old_page_source = driver_T.page_source
        
        ActionChains(driver_T).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver_T.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_T.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_T.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_T.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_T.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_T.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_T.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_T.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_T.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_T.append(bus.text)
        Route_links.append(link)
        Route_names.append(routes)
    for bus_type_elem in bus_type:
        Bus_types_T.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_T.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_T.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_T.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_T.append(ratings.text)
    for price_elem in price:
        Prices_T.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_T.append(seats_elem.text)
print("Successfully Completed")

# from list to convert data frame
data_3 = {
    'Bus_name': Bus_names_T,
    'Bus_type': Bus_types_T,
    'Start_time': Start_Time_T,
    'End_time': End_Time_T,
    'Total_duration': Total_Duration_T,
    'Price': Prices_T,
    "Seats_Available":Seats_Available_T,
    "Ratings":Ratings_T,
    'Route_link': Route_links,
    'Route_name': Route_names
}

df_buses_3 = pd.DataFrame(data_3)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_3.csv"
df_buses_3.to_csv(path,index=False)

df_buses_3

#open the browser -- kadamba  -- 4

driver_k=webdriver.Chrome()

#load the webpage
driver_k.get("https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile")

time.sleep(3)

driver_k.maximize_window()

#retrive bus links and route
wait = WebDriverWait(driver_k, 20)
def Kadamba_link_route(path):   
    Links_Kadamba=[]
    Route_Kadamba=[]
    
    for i in range(1,4):
        paths=driver_k.find_elements(By.XPATH,path)
        # retrive the route links 
        for links in paths:
            d = links.get_attribute("href")
            Links_Kadamba.append(d)
            
        # retrive names of the routes
        for route in paths:
            Route_Kadamba.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver_k.execute_script("arguments[0].scrollIntoView();", next_button)  
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_Kadamba,Route_Kadamba

Links_Kadamba,Route_Kadamba=Kadamba_link_route("//a[@class='route']")

df_G=pd.DataFrame({"Route_name":Route_Kadamba,"Route_link":Links_Kadamba})
df_G

path=r"D:/Subathra/DataScience/Redbus/df_G.csv"
df_G.to_csv(path,index=False)

# read the csv file
df_3=pd.read_csv("df_G.csv")
df_3

# retrive the bus details
driver_G = webdriver.Chrome()
Bus_names_G = []
Bus_types_G = []
Start_Time_G = []
End_Time_G = []
Ratings_G = []
Total_Duration_G = []
Prices_G = []
Seats_Available_G = []
Route_names = []
Route_links = []

for i,r in df_3.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]

# Loop through each link
    driver_G.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_G.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2)
   
    time.sleep(2)
    scrolling = True
    while scrolling:
        old_page_source = driver_G.page_source
        
        ActionChains(driver_G).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver_G.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_G.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_G.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_G.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_G.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_G.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_G.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_G.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_G.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_G.append(bus.text)
        Route_links.append(link)
        Route_names.append(routes)
    for bus_type_elem in bus_type:
        Bus_types_G.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_G.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_G.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_G.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_G.append(ratings.text)
    for price_elem in price:
        Prices_G.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_G.append(seats_elem.text)
print("Successfully Completed")

# from list to convert data frame
data_4 = {
    'Bus_name': Bus_names_G,
    'Bus_type': Bus_types_G,
    'Start_time': Start_Time_G,
    'End_time': End_Time_G,
    'Total_duration': Total_Duration_G,
    'Price': Prices_G,
    "Seats_Available":Seats_Available_G,
    "Ratings":Ratings_G,
    'Route_link': Route_links,
    'Route_name': Route_names
}

df_buses_4 = pd.DataFrame(data_4)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_4.csv"
df_buses_4.to_csv(path,index=False)

df_buses_4

#open the browser -- Rajasthan -- 5

driver_R=webdriver.Chrome()

#load the webpage
driver_R.get("https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile")

time.sleep(3)

driver_R.maximize_window()

#retrive bus links and route
wait = WebDriverWait(driver_R, 20)
def Rajastan_link_route(path):   
    Links_Rajastan=[]
    Route_Rajastan=[]
    
    for i in range(1,3):
        paths=driver_R.find_elements(By.XPATH,path)
        # retrive the route links 
        for links in paths:
            d = links.get_attribute("href")
            Links_Rajastan.append(d)
            
        # retrive names of the routes
        for route in paths:
            Route_Rajastan.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver_R.execute_script("arguments[0].scrollIntoView();", next_button)  
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_Rajastan,Route_Rajastan

Links_Rajastan,Route_Rajastan=Rajastan_link_route("//a[@class='route']")

df_R=pd.DataFrame({"Route_name":Route_Rajastan,"Route_link":Links_Rajastan})
df_R

path=r"D:/Subathra/DataScience/Redbus/df_R.csv"
df_R.to_csv(path,index=False)

# read the csv file
df_4=pd.read_csv("df_R.csv")
df_4

# retrive the bus details
driver_R = webdriver.Chrome()
Bus_names_R = []
Bus_types_R = []
Start_Time_R = []
End_Time_R = []
Ratings_R = []
Total_Duration_R = []
Prices_R = []
Seats_Available_R = []
Route_names_R = []
Route_links_R = []

for i,r in df_4.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]

# Loop through each link
    driver_R.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_R.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2)

    scrolling = True
    while scrolling:
        old_page_source = driver_R.page_source
        
        ActionChains(driver_R).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver_R.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_R.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_R.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_R.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_R.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_R.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_R.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_R.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_R.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_R.append(bus.text)
        Route_links_R.append(link)
        Route_names_R.append(routes)
    for bus_type_elem in bus_type:
        Bus_types_R.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_R.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_R.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_R.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_R.append(ratings.text)
    for price_elem in price:
        Prices_R.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_R.append(seats_elem.text)
print("Successfully Completed")

# from list to convert data frame
data_5 = {
    'Bus_name': Bus_names_R,
    'Bus_type': Bus_types_R,
    'Start_time': Start_Time_R,
    'End_time': End_Time_R,
    'Total_duration': Total_Duration_R,
    'Price': Prices_R,
    "Seats_Available":Seats_Available_R,
    "Ratings":Ratings_R,
    'Route_link': Route_links_R,
    'Route_name': Route_names_R
}

df_buses_5 = pd.DataFrame(data_5)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_5.csv"
df_buses_5.to_csv(path,index=False)

df_buses_5

#open the browser -- South Bengal -- 6

driver_SB=webdriver.Chrome()

#load the webpage
driver_SB.get("https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile")

time.sleep(3)

driver_SB.maximize_window()

#retrive  bus links and route
wait = WebDriverWait(driver_SB, 20)
def SouthBengal_link_route(path):   
    Links_SouthBengal=[]
    Route_SouthBengal=[]
     
    for i in range(1,6):
        paths=driver_SB.find_elements(By.XPATH,path)
        # retrive the route links
        for links in paths:
            d = links.get_attribute("href")
            Links_SouthBengal.append(d)
            
        # retrive names of the routes
        for route in paths:
            Route_SouthBengal.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver_SB.execute_script("arguments[0].scrollIntoView();", next_button)  
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_SouthBengal,Route_SouthBengal

Links_SouthBengal,Route_SouthBengal=SouthBengal_link_route("//a[@class='route']")

df_SB=pd.DataFrame({"Route_name":Route_SouthBengal,"Route_link":Links_SouthBengal})
df_SB

path=r"D:/Subathra/DataScience/Redbus/df_SB.csv"
df_SB.to_csv(path,index=False)

# read the csv file
df_5=pd.read_csv("df_SB.csv")
df_5

# retrive the bus details
driver_SB = webdriver.Chrome()
Bus_names_SB = []
Bus_types_SB = []
Start_Time_SB = []
End_Time_SB = []
Ratings_SB = []
Total_Duration_SB = []
Prices_SB = []
Seats_Available_SB = []
Route_names = []
Route_links = []

for i,r in df_5.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]

# Loop through each link
    driver_SB.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_SB.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2)
    
    scrolling = True
    while scrolling:
        old_page_source = driver_SB.page_source
        
        ActionChains(driver_SB).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver_SB.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_SB.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_SB.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_SB.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_SB.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_SB.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_SB.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_SB.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_SB.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_SB.append(bus.text)
        Route_links.append(link)
        Route_names.append(routes)
    for bus_type_elem in bus_type:
        Bus_types_SB.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_SB.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_SB.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_SB.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_SB.append(ratings.text)
    for price_elem in price:
        Prices_SB.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_SB.append(seats_elem.text)
print("Successfully Completed")

# from list to convert data frame
data_6 = {
    'Bus_name': Bus_names_SB,
    'Bus_type': Bus_types_SB,
    'Start_time': Start_Time_SB,
    'End_time': End_Time_SB,
    'Total_duration': Total_Duration_SB,
    'Price': Prices_SB,
    "Seats_Available":Seats_Available_SB,
    "Ratings":Ratings_SB,
    'Route_link': Route_links,
    'Route_name': Route_names
}

df_buses_6 = pd.DataFrame(data_6)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_6.csv"
df_buses_6.to_csv(path,index=False)

df_buses_6

# Open the browser -- Haryana -- 7

driver_H = webdriver.Chrome()

# Load the webpage
driver_H.get("https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile")

time.sleep(3)

driver_H.maximize_window()

# Retrieve bus links and routes
wait = WebDriverWait(driver_H, 20)

def Haryana_link_route(path):   
    Links_Haryana = []
    Route_Haryana = []
    
    for i in range(1, 6):
        paths = driver_H.find_elements(By.XPATH, path)
        
        # Retrieve the route links 
        for links in paths:
            d = links.get_attribute("href")
            Links_Haryana.append(d)
        
        # Retrieve names of the routes
        for route in paths:
            Route_Haryana.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver_H.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_Haryana, Route_Haryana

Links_Haryana, Route_Haryana = Haryana_link_route("//a[@class='route']")

df_H=pd.DataFrame({"Route_name":Route_Haryana,"Route_link":Links_Haryana})
df_H

path=r"D:/Subathra/DataScience/Redbus/df_H.csv"
df_H.to_csv(path,index=False)

# read the csv file
df_6=pd.read_csv("df_H.csv")
df_6

# retrive the bus details
driver_H = webdriver.Chrome()
Bus_names_H = []
Bus_types_H = []
Start_Time_H = []
End_Time_H = []
Ratings_H = []
Total_Duration_H = []
Prices_H = []
Seats_Available_H = []
Route_names_H = []
Route_links_H = []
for i,r in df_6.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]

# Loop through each link
    driver_H.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_H.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2)
         
    scrolling = True
    while scrolling:
        old_page_source = driver_H.page_source
        
        ActionChains(driver_H).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver_H.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_H.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_H.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_H.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_H.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_H.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_H.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_H.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_H.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_H.append(bus.text)
        Route_links_H.append(link)
        Route_names_H.append(routes)
    for bus_type_elem in bus_type:
        Bus_types_H.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_H.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_H.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_H.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_H.append(ratings.text)
    for price_elem in price:
        Prices_H.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_H.append(seats_elem.text)
print("Successfully Completed")

# from list to convert data frame
data_7 = {
    'Bus_name': Bus_names_H,
    'Bus_type': Bus_types_H,
    'Start_time': Start_Time_H,
    'End_time': End_Time_H,
    'Total_duration': Total_Duration_H,
    'Price': Prices_H,
    "Seats_Available":Seats_Available_H,
    "Ratings":Ratings_H,
    'Route_link': Route_links_H,
    'Route_name': Route_names_H
}

df_buses_7 = pd.DataFrame(data_7)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_7.csv"
df_buses_7.to_csv(path,index=False)

df_buses_7

#open the browser -- Assam -- 8

driver_AS=webdriver.Chrome()

#load the webpage

driver_AS.get("https://www.redbus.in/online-booking/astc/?utm_source=rtchometile")

time.sleep(3)

driver_AS.maximize_window()

#retrive bus links and route
wait = WebDriverWait(driver_AS, 20)
def Assam_link_route(path):   
    Links_Assam=[]
    Route_Assam=[]
    
    for i in range(1,5):
        paths=driver_AS.find_elements(By.XPATH,path)
        # retrive the route links 
        for links in paths:
            d = links.get_attribute("href")
            Links_Assam.append(d)
            
        # retrive names of the routes
        for route in paths:
            Route_Assam.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver_AS.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_Assam,Route_Assam

Links_Assam,Route_Assam=Assam_link_route("//a[@class='route']")

df_AS=pd.DataFrame({"Route_name":Route_Assam,"Route_link":Links_Assam})
df_AS

path=r"D:/Subathra/DataScience/Redbus/df_AS.csv"
df_AS.to_csv(path,index=False)

# read the csv file
df_7=pd.read_csv("df_AS.csv")
df_7

# retrive the bus details
driver_AS = webdriver.Chrome()
Bus_names_AS = []
Bus_types_AS = []
Start_Time_AS = []
End_Time_AS = []
Ratings_AS = []
Total_Duration_AS = []
Prices_AS = []
Seats_Available_AS = []
Route_names_AS = []
Route_links_AS = []
for i,r in df_7.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]
# Loop through each link
    driver_AS.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_AS.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2)
         
    scrolling = True
    while scrolling:
        old_page_source = driver_AS.page_source
        
        ActionChains(driver_AS).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver_AS.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_AS.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_AS.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_AS.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_AS.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_AS.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_AS.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_AS.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_AS.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_AS.append(bus.text)
        Route_links_AS.append(link)
        Route_names_AS.append(routes)
    for bus_type_elem in bus_type:
        Bus_types_AS.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_AS.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_AS.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_AS.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_AS.append(ratings.text)
    for price_elem in price:
        Prices_AS.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_AS.append(seats_elem.text)
print("Successfully Completed")

# from list to convert data frame
data_8 = {
    'Bus_name': Bus_names_AS,
    'Bus_type': Bus_types_AS,
    'Start_time': Start_Time_AS,
    'End_time': End_Time_AS,
    'Total_duration': Total_Duration_AS,
    'Price': Prices_AS,
    "Seats_Available":Seats_Available_AS,
    "Ratings":Ratings_AS,
    'Route_link': Route_links_AS,
    'Route_name': Route_names_AS
}

df_buses_8 = pd.DataFrame(data_8)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_8.csv"
df_buses_8.to_csv(path,index=False)

df_buses_8

#open the browser -- UP -- 9

driver_UP=webdriver.Chrome()

#load the webpage

driver_UP.get("https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile")

time.sleep(3)

driver_UP.maximize_window()

#retrive bus links and route
wait = WebDriverWait(driver_UP, 20)
def UP_link_route(path):   
    Links_UP=[]
    Route_UP=[]
    
    for i in range(1,6):
        paths=driver_UP.find_elements(By.XPATH,path)
        # retrive the route links 
        for links in paths:
            d = links.get_attribute("href")
            Links_UP.append(d)
            
        # retrive names of the routes
        for route in paths:
            Route_UP.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver_UP.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_UP,Route_UP

Links_UP,Route_UP=UP_link_route("//a[@class='route']")

df_UP=pd.DataFrame({"Route_name":Route_UP,"Route_link":Links_UP})
df_UP

path=r"D:/Subathra/DataScience/Redbus/df_UP.csv"
df_UP.to_csv(path,index=False)

# read the csv file
df_8=pd.read_csv("df_UP.csv")
df_8

# retrive the bus details
driver_UP = webdriver.Chrome()
Bus_names_UP = []
Bus_types_UP = []
Start_Time_UP = []
End_Time_UP = []
Ratings_UP = []
Total_Duration_UP = []
Prices_UP = []
Seats_Available_UP = []
Route_names = []
Route_links = []

for i,r in df_8.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]

# Loop through each link
    driver_UP.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_UP.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2) 
        
    scrolling = True
    while scrolling:
        old_page_source = driver_UP.page_source
        
        ActionChains(driver_UP).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver_UP.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_UP.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_UP.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_UP.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_UP.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_UP.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_UP.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_UP.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_UP.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_UP.append(bus.text)
        Route_links.append(link)
        Route_names.append(routes)
    for bus_type_elem in bus_type:
        Bus_types_UP.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_UP.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_UP.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_UP.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_UP.append(ratings.text)
    for price_elem in price:
        Prices_UP.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_UP.append(seats_elem.text)
print("Successfully Completed")

# from list to convert data frame
data_9 = {
    'Bus_name': Bus_names_UP,
    'Bus_type': Bus_types_UP,
    'Start_time': Start_Time_UP,
    'End_time': End_Time_UP,
    'Total_duration': Total_Duration_UP,
    'Price': Prices_UP,
    "Seats_Available":Seats_Available_UP,
    "Ratings":Ratings_UP,
    'Route_link': Route_links,
    'Route_name': Route_names
}

df_buses_9 = pd.DataFrame(data_9)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_9.csv"
df_buses_9.to_csv(path,index=False)

df_buses_9

# Open the browser -- West Bengal -- 10

driver_WB = webdriver.Chrome()

# Load the webpage
driver_WB.get("https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile")

time.sleep(3)

driver_WB.maximize_window() 

# Retrieve bus links and routes
wait = WebDriverWait(driver_WB, 20)

def Westbengal_link_route(path):   
    Links_Westbengal = []
    Route_Westbengal = []
    
    for i in range(1, 6):
        paths = driver_WB.find_elements(By.XPATH, path)
        
        # Retrieve the route links 
        for links in paths:
            d = links.get_attribute("href")
            Links_Westbengal.append(d)
        
        # Retrieve names of the routes
        for route in paths:
            Route_Westbengal.append(route.text)
            
        try:
            # Wait for the pagination element to be present
            pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
            next_button = pagination.find_element(By.XPATH, f'//div[@class="DC_117_pageTabs " and text()={i+1}]')
            time.sleep(3)
            driver_WB.execute_script("arguments[0].scrollIntoView();", next_button)  # Scroll to the next button
            time.sleep(1)  # Give some time for the scroll action
            
            # Click the next button
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            
        except NoSuchElementException:
            print(f"No more pages to paginate at step {i}")
            break
            
    return Links_Westbengal, Route_Westbengal

Links_Westbengal, Route_Westbengal = Westbengal_link_route("//a[@class='route']")

df_WB=pd.DataFrame({"Route_name":Route_Westbengal,"Route_link":Links_Westbengal})
df_WB

path=r"D:/Subathra/DataScience/Redbus/df_WB.csv"
df_WB.to_csv(path,index=False)

# read the csv file
df_9=pd.read_csv("df_WB.csv")
df_9

# retrive the bus details
driver_WB = webdriver.Chrome()
Bus_names_WB = []
Bus_types_WB = []
Start_Time_WB = []
End_Time_WB = []
Ratings_WB = []
Total_Duration_WB = []
Prices_WB = []
Seats_Available_WB = []
Route_names = []
Route_links = []

for i,r in df_9.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]
# Loop through each link
    driver_WB.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver_WB.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2) 
        
    scrolling = True
    while scrolling:
        old_page_source = driver_WB.page_source
        
        ActionChains(driver_WB).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver_WB.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    bus_name = driver_WB.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bus_type = driver_WB.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    start_time = driver_WB.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    end_time = driver_WB.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    total_duration = driver_WB.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        rating = driver_WB.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver_WB.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seats = driver_WB.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in bus_name:
        Bus_names_WB.append(bus.text)
        Route_links.append(link)
        Route_names.append(routes)
    for bus_type_elem in bus_type:
        Bus_types_WB.append(bus_type_elem.text)
    for start_time_elem in start_time:
        Start_Time_WB.append(start_time_elem.text)
    for end_time_elem in end_time:
        End_Time_WB.append(end_time_elem.text)
    for total_duration_elem in total_duration:
        Total_Duration_WB.append(total_duration_elem.text)
    for ratings in rating:
        Ratings_WB.append(ratings.text)
    for price_elem in price:
        Prices_WB.append(price_elem.text)
    for seats_elem in seats:
        Seats_Available_WB.append(seats_elem.text)
print("Successfully Completed")

# from list to convert data frame
data_10 = {
    'Bus_name': Bus_names_WB,
    'Bus_type': Bus_types_WB,
    'Start_time': Start_Time_WB,
    'End_time': End_Time_WB,
    'Total_duration': Total_Duration_WB,
    'Price': Prices_WB,
    "Seats_Available":Seats_Available_WB,
    "Ratings":Ratings_WB,
    'Route_link': Route_links,
    'Route_name': Route_names
}

df_buses_10 = pd.DataFrame(data_10)
#convert dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_buses_10.csv"
df_buses_10.to_csv(path,index=False)

df_buses_10

# concat all the bus link and route names in one dataframe
df=pd.concat([df_k,df_A,df_T,df_G,df_R,df_H,df_SB,df_AS,df_UP,df_WB],ignore_index=True)
df

# change dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/df_route.csv"
df.to_csv(path,index=False)