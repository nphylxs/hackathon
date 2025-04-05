from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time

def time_conv(user):
    result = f'{user[0:2]}%3A{user[3:5]}'
    return result

#function to find links for available times
def available():
    #empty list where we can store links for the buttons
    urls = []
    #find buttons
    availability = driver.find_elements(By.CLASS_NAME, "s-lc-suggestion-book-now")
    #loooping through each button
    for index, button in enumerate(availability):
        #opening in a new tab
        ActionChains(driver).key_down(Keys.CONTROL).click(availability[index]).key_up(Keys.CONTROL).perform()
        time.sleep(2)
        #switch to new tab
        driver.switch_to.window(driver.window_handles[-1])
        #get the url
        current_url = driver.current_url
        urls.append(current_url)
        
    return urls

def unavailable():
    #empty dictionaries
    urls = {}
    #taking their times
    times = driver.find_elements(By.CLASS_NAME, "s-lc-booking-other-time margin-right-med")

    availability = driver.find_elements(By.CLASS_NAME, "s-lc-suggestion-book-now")
    #loooping through each button
    for index, button in enumerate(availability):
        #opening in a new tab
        ActionChains(driver).key_down(Keys.CONTROL).click(availability[index]).key_up(Keys.CONTROL).perform()
        time.sleep(2)
        #switch to new tab
        driver.switch_to.window(driver.window_handles[-1])
        #get the url
        current_url = driver.current_url
        urls[times[index].text] = current_url
    return urls
#asking for preferred time and date
date = input('Enter the date: ') #must be in YYYY-MM-DD format
start = time_conv(input('Start time: '))#must be in 24 hour format
end = time_conv(input('End time: ')) #must be in 24 hour format
#people = int(input('How many people?(1-6) '))
#capacity = 1 if people <= 2 else 2

date = '2025-04-05'
start = time_conv('18:00')#must be in 24 hour format
end = time_conv('19:15') #must be in 24 hour format
capacity = 2

driver = webdriver.Chrome()
link = f'https://calendar.lib.usf.edu/spaces?m=t&lid=1729&gid=19125&capacity={capacity}&zone=0&date={date}&date-end={date}&start={start}&end={end}'

#open the url
driver.get(link)

time.sleep(4)


try:
    # Look for the "no rooms" warning
    no_rooms_element = driver.find_element(By.XPATH, "//*[contains(text(), 'no results available for the selected date & time')]")
    print("No rooms available for the selected time.")
    rooms = unavailable()
except NoSuchElementException:
    print("Rooms might be available!")
    rooms = available()
    
    
if isinstance(rooms, list):
    for i, url in enumerate(rooms):
        print('List')
        print(f'{i}: {url}')
elif isinstance(rooms, dict):
    print(rooms)
    for i in rooms:
        print(f'{i}: {rooms[i]}')

    

driver.quit()