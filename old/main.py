import requests
import bs4

headers={'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
URL = "https://www.mp.cz/tablet-apple-ipad-air-2020-64gb-wi-fi-rose-gold-a-pouzity-p-115480"
page = requests.get(URL, headers=headers)

print(page.text)