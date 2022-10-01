import requests
from bs4 import BeautifulSoup

linkOfItem = "https://www.eurotech.cz/dell-xps-13-9370-ssd-4k-1/?gclid=Cj0KCQjwmdGYBhDRARIsABmSEeNMLUkjxnP9teqmo37NzBsRouyBCztx6qFxWtYfa8hoCxnsOKKcOVEaAvH0EALw_wcB"

# get page
page = requests.get(linkOfItem)

# price of item
## get data
soup = BeautifulSoup(page.content, "html.parser")
priceOfItem = soup.find(id="detail_cenas")

## format data
priceOfItem = str(priceOfItem)
priceOfItem = priceOfItem[24:]
priceOfItem = priceOfItem[:6]
priceOfItem = priceOfItem + " Kč"

## print data
print(priceOfItem)

# state of item
## get data
stateOfItem = soup.find(id="id_dostupnost")

## format data
stateOfItem = str(stateOfItem)
stateOfItem = stateOfItem[73:]
stateOfItem = stateOfItem[:14]
if stateOfItem == "ihned k odběru":
    stateOfItem = "Skladem"

## print data
print(stateOfItem)




