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

lineCount = 0
with open('links.txt') as f:
    lines = f.readline(lineCount)
    lineCount += 1


options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

executablePathWebDriverChrome = 'D:\Dokumenty\Kódování\Python\iPad Web Scraper\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=executablePathWebDriverChrome)
driver.implicitly_wait(10)

driver.get("https://www.mp.cz/tablet-apple-ipad-air-2020-64gb-wi-fi-rose-gold-a-pouzity-p-115480")

wait = WebDriverWait(driver, 15)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cms-app"]/div[2]/div/div/div/div[3]/button[1]')))
driver.find_element("xpath", '//*[@id="cms-app"]/div[2]/div/div/div/div[3]/button[1]').click()

driver.implicitly_wait(10)

stateXPath = '//*[@id="component-43773"]/div/div[1]/div[2]/div/div[6]/div[1]/div[1]/div/div/span'
priceXPath = '//*[@id="component-43773"]/div/div[1]/div[2]/div/div[6]/div[1]/div[2]/div'

print(driver.find_element("xpath", stateXPath).text)
print(driver.find_element("xpath", priceXPath).text)


driver.save_screenshot('hn_homepage.png')
driver.quit()
