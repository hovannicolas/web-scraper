import requests
from bs4 import BeautifulSoup
from csv import writer

response = requests.get("http://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")
quotes = (soup.find_all(class_="quote"))
all_quotes =[]

for quote in quotes:
    all_quotes.append({
        "text": quote.find(class_="text").get_text(),
        "author": quote.find(class_="author").get_text(),
        "bio-href": quote.find(class_="a")
    })
print(all_quotes)




