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
import tkinter as tk
from tkinter import ttk
import sv_ttk
import csv
from tkinter import *
import tkinter.ttk as ttk
import csv
from datetime import datetime


def GUI2Function():
    root = Tk()
    root.title("Parium - MobilPohotovost Watchdog v0.1.2-alpha")
    width = 720
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)

    TableMargin = Frame(root, width=720)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("Date", "Name", "Class", "State", "Price"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Date', text="Date", anchor=W)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Class', text="Class", anchor=W)
    tree.heading('State', text="State", anchor=W)
    tree.heading('Price', text="Price", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=120)
    tree.column('#2', stretch=NO, minwidth=0, width=300)
    tree.column('#3', stretch=NO, minwidth=0, width=50)
    tree.column('#4', stretch=NO, minwidth=0, width=160)
    tree.column('#5', stretch=NO, minwidth=0, width=60)
    tree.pack()

    with open('metadata.csv', encoding='UTF8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            time = row['time']
            name = row['nameOfItem']
            classi = row['classOfItem']
            state = row['stateOfItem']
            price = row['priceOfItem']
            tree.insert("", 0, values=(time, name, classi, state, price))
    if __name__ == '__main__':
        root.mainloop()

def main():
    # create runtime window
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    # chrome web driver location, if installed someplace else, can be changed, use relative location
    executablePathWebDriverChrome = './chromedriver_win32/chromedriver.exe'
    driver = webdriver.Chrome(options=options, executable_path=executablePathWebDriverChrome)
    driver.implicitly_wait(10)

    # opens website based on link created within the main loop
    driver.get(linkOfItem)

    # individial eshop data input layers
    if eshop == "mobilPohotovost":
        ## cookie accept for screenshot
        wait = WebDriverWait(driver, 15)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cms-app"]/div[2]/div/div/div/div[3]/button[1]')))
        driver.find_element("xpath", '//*[@id="cms-app"]/div[2]/div/div/div/div[3]/button[1]').click()
        driver.implicitly_wait(10)
        ## xpath element location
        stateXPath = '//*[@id="component-43773"]/div/div[1]/div[2]/div/div[6]/div[1]/div[1]/div/div/span'
        priceXPath = '//*[@id="component-43773"]/div/div[1]/div[2]/div/div[6]/div[1]/div[2]/div'
        ## gets availibilty and price data
        stateOfItem = driver.find_element("xpath", stateXPath).text
        priceOfItem = driver.find_element("xpath", priceXPath).text
        ## compatibility layer
        if stateOfItem.startswith("Prodej pouze na"):
            stateOfItem = "Omezený prodej"
    
    if eshop == "eurotech":
        ## xpath element location
        stateXPath = '//*[@id="id_dostupnost"]'
        priceXPath = '//*[@id="detail_cenas"]'
        ## fixes for aesthetics
        stateOfItem = stateOfItem.capitalize()
        priceOfItem = priceOfItem + " Kč"
        ## gets availibilty and price data
        stateOfItem = driver.find_element("xpath", stateXPath).text
        priceOfItem = driver.find_element("xpath", priceXPath).text

    if eshop == "czc":
        ## xpath or css selector element location
        priceXPath = '//*[@id="product-price-and-delivery-section"]/div[3]/div/span/span[2]'
        stateSelectorPath = '#warehouse > span'
        ## gets availibilty and price data
        priceOfItem = driver.find_element("xpath", priceXPath).text
        stateOfItem = driver.find_element("css selector", stateSelectorPath).text
        ## fixes for aesthetics
        if stateOfItem.startswith("Skladem"):
            stateOfItem = "Skladem"

    if eshop == "levnaPC":
        ## xpath or css selector element location
        priceXPath = '//*[@id="spanTotalPriceAndTax"]'
        stateSelectorPath = 'body > div.Content > div.Main > div.MainRight > div.ProductPage > div.ProductTopPanel > div.ProductInfo > font > b'
        ## gets availibilty and price data
        priceOfItem = driver.find_element("xpath", priceXPath).text
        stateOfItem = driver.find_element("css selector", stateSelectorPath).text
        ## fixes for aesthetics
        priceOfItem = priceOfItem.rstrip(',-')
        priceOfItem = priceOfItem + " Kč"
        priceOfItem = priceOfItem[1:]
        ## compatibility for availibility count
        stateOfItemNumber = int(stateOfItem) 
        if stateOfItemNumber >= 1:
            stateOfItem = "Skladem"


    # locates availibility and price by xpath
    stateOfItem = driver.find_element("xpath", stateXPath).text
    priceOfItem = driver.find_element("xpath", priceXPath).text

    # create data input for csv table
    ## variable has to be global as it is the main variable of the whole program
    global overviewOfItem
    overviewOfItem   = nameOfItem + " " + classOfItem + " " + stateOfItem + " " + priceOfItem

    # make a screenshot from the website
    ## screenshot name with relative location dependent on the main.exe/main.py location
    screenshotName = './screenshots/Screenshot ' + str(datetime.now())[0:-7] + '.png'
    ## fix compatibility for names within file subsystem
    screenshotName = screenshotName.replace(" ", "_").replace(":", "_").replace("-", "_")
    ## make the actual screenshot and quit driver session
    driver.save_screenshot(screenshotName)
    driver.quit()

    # counting circuit for csv table data (so far unutilised)
    global count

    # data for csv table formatter
    if nameOfItem.startswith("Apple Mac"):
        count += 1
        # macbook compatibility layer (legacy)
        data = [str(datetime.now())[0:-7], count, nameOfItem[6:], classOfItem[-1], stateOfItem, priceOfItem]
    else:
        count += 1
        data = [str(datetime.now())[0:-7], count, nameOfItem, classOfItem[-1], stateOfItem, priceOfItem]

    # data for csv table inputter
    f = open("metadata.csv", "a", encoding='UTF8')
    writer = csv.writer(f)
    writer.writerow(data)

with open('links.txt', 'r', encoding='utf8') as f:
    global count
    count = 0
    timestamp = datetime.now()
    for line in f:
        contents = line.strip()
        contentType = ''
        if contents.startswith('https') == True:
            contentType = 'link'
            linkOfItem = contents
            timestamp = datetime.now()
            if linkOfItem.startswith('https://www.mp.cz/'):
                eshop = 'mobilPohotovost'
            if linkOfItem.startswith('https://www.eurotech.cz/'):
                eshop = 'eurotech'
            if linkOfItem.startswith('https://www.levnapc.cz/'):
                eshop = 'levnaPC'
            if linkOfItem.startswith('https://www.czc.cz/'):
                eshop = 'czc'
            main()
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
        if contents.startswith('***'):
            break

GUI2Function()
