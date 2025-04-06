from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time

def time_conv(user):
    result = f'{user[0:2]}%3A{user[3:5]}'
    return result

def initial(date, start, end, people):
    start = time_conv(start)#must be in 24 hour format
    end = time_conv(end) #must be in 24 hour format
    capacity = 1 if people <= 2 else 2
    
    driver = webdriver.Chrome()
    
    link = f'https://calendar.lib.usf.edu/spaces?m=t&lid=1729&gid=19125&capacity={capacity}&zone=0&date={date}&date-end={date}&start={start}&end={end}'

    #open the url
    driver.get(link)
    try:
        # Look for the "no rooms" warning
        no_rooms_element = driver.find_element(By.XPATH, "//*[contains(text(), 'no results available for the selected date & time')]")
        print("No rooms available for the selected time.")
    except NoSuchElementException:
        print("Rooms might be available!")
        rooms = available(driver)
        for i in rooms:
            print('List')
            print(f'{i}: {rooms[i]}')

def available(driver):
    #empty list where we can store links for the buttons
    urls = []
    #for headings
    titles = []
    #find buttons
    availability = driver.find_elements(By.CLASS_NAME, "s-lc-suggestion-book-now")
    #find headings
    headings = driver.find_elements(By.CLASS_NAME, "s-lc-suggestion-heading")
    for heading in headings:
        room_name = heading.find_element(By.TAG_NAME, "a").text
        titles.append(room_name)
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
        
    driver.quit()
    return dict(zip(titles, urls))


import json
from groq import Groq
import groq
def analyser():
    #to access groq
    filename = f"schedule.json"
    
    #the prompt that specifies everything to groq
    prompt =(
        "I am going to send you a JSON file of a person's schedule"
        "You must suggest a time for them to study for the various classes that they are taking"
        "You must also take into account when a human mind is the most ready for studying"
        "Return the answer in JSON format with only suggested study times"
        "for example:"
        "{\n"
        "  'date': 'YYYY-MM-DD',\n"
        "  'start': '<HH:MM, 24 hour format>',\n"
        "  'end': '<HH:MM, 24 hour format>',\n"
        "  'subject': '<subject_name>',\n"
        "} \n"
    )
    #loading the data into memory
    with open(filename, "r") as f:
        data = json.load(f)
        answer = ai_portion(prompt, data)
    return answer

def ai_portion(prompt, data):
    #setting up
    client = Groq(
        api_key= "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"
    )
    #sending the prompt
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt} Here is the data: {data}",
            }
        ],
        model="llama3-8b-8192",
    )
    #receiving output from groq
    content = chat_completion.choices[0].message.content
    return content