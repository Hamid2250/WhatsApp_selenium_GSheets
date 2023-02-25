from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from config import BASE_URL, CHROME_DATA_PATH
from time import sleep
from replays import process_message


chrome_path = r"C:\Hamid\autotask\ai_auto\WhatsApp_selenium_GSheets\chromedriver.exe"
service = Service(chrome_path)
options = webdriver.ChromeOptions()
options.add_argument(CHROME_DATA_PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.get(BASE_URL)
driver.implicitly_wait(20)

def check_new_message():
    if driver.find_element(By.XPATH, '//*[@id="pane-side"]/div/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/span[1]/div'):
        return True
    else:
        return False
    
def get_message():
    new_message = driver.find_element(By.XPATH, '//*[@id="pane-side"]/div/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/span[1]/div')
    new_message.click()
    driver.implicitly_wait(5)
    
    # Find the chat window element
    chat_window = driver.find_element(By.XPATH, '//*[@id="main"]')

    # Get all the messages in the chat window
    # messages = chat_window.find_elements(By.CSS_SELECTOR, 'div[class="n5hs2j7m oq31bsqd gx1rr48f qh5tioqs"]')
    # print(list(messages))
    # # Get the last message in the chat window
    # last_message = messages[-1]
    
    # Get the text of the last message
    last_message_text = chat_window.find_element(By.CSS_SELECTOR, 'div[class="message-in focusable-list-item _7GVCb _2SnTA _1-FMR"]').text
    last_message_text = last_message_text.split('\n')
    
    # Get the user
    user = chat_window.find_element(By.CSS_SELECTOR, 'span[class="ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr _11JPr"]').text

    return last_message_text, user

def reply(message):
    # Type and send message
    message_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    driver.implicitly_wait(5)
    message_box.send_keys(str(message))
    driver.implicitly_wait(5)
    message_box.send_keys(Keys.ENTER)
    sleep(5)
    
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
        # check_new_message()
        message, user = get_message()
        sleep(1)
        print(f"get {message[0]}")
        message = process_message(message[0], user)
        print(message)
        reply(message)
        # send_message("+966538192825", "Hi John, how are you?")
    except Exception:
        # Close browser
        driver.quit()
        sleep(5)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(BASE_URL)

