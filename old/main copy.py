from os import link
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup #pip install beautifulsoup4
import PySimpleGUI as sg

def mainFunction():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    executablePathWebDriverChrome = 'D:\Dokumenty\Kódování\Python\iPad Web Scraper\chromedriver_win32\chromedriver.exe'
    driver = webdriver.Chrome(options=options, executable_path=executablePathWebDriverChrome)
    driver.implicitly_wait(10)

    driver.get(linkOfItem)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cms-app"]/div[2]/div/div/div/div[3]/button[1]')))
    driver.find_element("xpath", '//*[@id="cms-app"]/div[2]/div/div/div/div[3]/button[1]').click()

    driver.implicitly_wait(10)

    stateXPath = '//*[@id="component-43773"]/div/div[1]/div[2]/div/div[6]/div[1]/div[1]/div/div/span'
    priceXPath = '//*[@id="component-43773"]/div/div[1]/div[2]/div/div[6]/div[1]/div[2]/div'

    stateOfItem = driver.find_element("xpath", stateXPath).text
    if stateOfItem.startswith("Prodej pouze na 1 prodejně"):
        stateOfItem = stateOfItem.rstrip("\n Z důvodu omezené dostupnosti je možný pouze osobní nákup na vybraných prodejnách")
    priceOfItem = driver.find_element("xpath", priceXPath).text
    print(nameOfItem, classOfItem, stateOfItem, priceOfItem)
    global overviewOfItem
    overviewOfItem   = nameOfItem + " " + classOfItem + " " + stateOfItem + " " + priceOfItem
    print(overviewOfItem)
    GUIFunction()

    driver.save_screenshot('hn_homepage.png')
    driver.quit()
    writeFunction()

def GUIFunction():
    layout = [[sg.Text(overviewOfItem)], [sg.Button("OK")]]
    window = sg.Window("Demo", layout)
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()

def writeFunction():
    text_file = open("metadata.txt", "a", encoding='utf8')
    text_file.write(overviewOfItem)
    text_file.write("\n")
    text_file.close()

with open('links.txt', 'r', encoding='utf8') as f:
    for line in f:
        contents = line.strip()
        contentType = ''
        if contents.startswith('https') == True:
            contentType = 'link'
            linkOfItem = contents
            mainFunction()
        if contents.startswith('-') == True:
            contentType = 'divider'
        if contents.startswith('name') == True:
            contentType = 'name'
            nameOfItem = contents
            nameOfItem = nameOfItem[5:]
        if contents.startswith('class') == True:
            contentType = 'class'
            classOfItem = contents
            classOfItem = classOfItem[6:]
