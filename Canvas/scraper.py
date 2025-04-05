from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time

def time_conv(user):
    result = f'{user[0:2]}%3A{user[3:5]}'
#asking for preferred time and date
date = input('Enter the date: ') #must be in YYYY-MM-DD format
start = input('Start time: ') #must be in 24 hour format
end = input('End time: ') #must be in 24 hour format
people = int(input('How many people?(1-6) '))
capacity = 1 if people <= 2 else 2

driver = webdriver.Chrome()
link = f'https://calendar.lib.usf.edu/spaces?m=t&lid=1729&gid=19125&capacity={capacity}&zone=0&date={date}&date-end={date}&start={start}&end={end}'

#open the url
driver.get(link)

time.sleep(4)


try:
    # Look for the "no rooms" warning
    no_rooms_element = driver.find_element(By.XPATH, "//*[contains(text(), 'no results available for the selected date & time')]")
    print("No rooms available for the selected time.")
except NoSuchElementException:
    print("Rooms might be available!")


#find buttons
availability = driver.find_elements(By.CLASS_NAME, "s-lc-suggestion-book-now")
#loooping through each button
for index, button in enumerate(availability):
     #opening in a new tab
    ActionChains(driver).key_down(Keys.CONTROL).click(availability[index]).key_up(Keys.CONTROL).perform()
    time.sleep(2)
    #switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    

driver.quit()