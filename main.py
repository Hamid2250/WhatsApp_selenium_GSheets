import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from config import BASE_URL, CHROME_DATA_PATH
from time import sleep
from replys import process_message


chrome_path = f"{os.getcwd()}\\chromedriver.exe"
service = Service(chrome_path)
options = webdriver.ChromeOptions()
options.add_argument(CHROME_DATA_PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.get(BASE_URL)
driver.implicitly_wait(20)

def get_message():
    # Check for new messages
    new_message = driver.find_element(By.XPATH, '//*[@id="pane-side"]/div/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/span[1]/div')
    new_message.click()
    driver.implicitly_wait(5)

    # Find the chat window element
    chat_window = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]')

    # Get the text of the last message
    last_message_text = chat_window.find_elements(By.CSS_SELECTOR, 'div[class="message-in focusable-list-item _7GVCb _2SnTA _1-FMR"]')
    last_message_text = last_message_text[-1].find_element(By.CSS_SELECTOR, 'span[class="_11JPr selectable-text copyable-text"]').text    
    last_message_text = list(last_message_text.split('\n'))

    # Get the user
    user = driver.find_element(By.CSS_SELECTOR, 'span[class="ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr _11JPr"]').text
    return last_message_text, user

def close_chat():
    # Find the chat header element
    chat_header = driver.find_element(By.CSS_SELECTOR, 'header[class="_23P3O"]')

    # Get Menu and click it
    chat_menu = chat_header.find_element(By.CSS_SELECTOR, 'span[class="kiiy14zj"]')
    chat_menu.click()

    # Get Close Chat Button and click it
    driver.implicitly_wait(5)
    close_chat_text = driver.find_element(By.XPATH, '//*[@id="app"]/div/span[4]/div/ul/div/div/li[3]/div')
    close_chat_text.click()
    

def reply(message):
    # Type and send message
    message_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    message_box.click()
    # driver.implicitly_wait(5)
    message_box.send_keys(message)
    # driver.implicitly_wait(5)
    message_box.send_keys(Keys.ENTER)
    sleep(1)

def send_message(name, message):
    # Search for user by name and click on chat
    search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div')
    search_box.click()
    driver.implicitly_wait(5)
    search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]')
    driver.implicitly_wait(5)
    search_box.send_keys(str(name))
    driver.implicitly_wait(5)  # Wait for search results to appear
    search_box.send_keys(Keys.ENTER)
    driver.implicitly_wait(5)

    # Type and send message
    message_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    driver.implicitly_wait(5)
    message_box.send_keys(message)
    driver.implicitly_wait(5)
    message_box.send_keys(Keys.ENTER)
    sleep(1)


while True:
    try:
        driver.implicitly_wait(20)
        message, user = get_message()
        message = process_message(message, user)
        reply(message)
        driver.implicitly_wait(5)
        close_chat()
        # driver.get(BASE_URL)
        # send_message("+966538192825", "Hi John, how are you?")
    except Exception:
        sleep(0.2)

# Close browser
# driver.quit()
