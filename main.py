import requests
from bs4 import BeautifulSoup
from csv import writer

all_quotes =[]
base_url = "http://quotes.toscrape.com"
url = "/page/1"

while url:
    response = requests.get(f"{base_url}{url}")
    print(f"Now scraping {base_url}{url}...")
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = (soup.find_all(class_="quote"))

    for quote in quotes:
        all_quotes.append({
        "text": quote.find(class_="text").get_text(),
        "author": quote.find(class_="author").get_text(),
        "bio-href": quote.find(class_="a")
        })
    next_btn = soup.find(class_="next")
    url = next_btn.find("a")["href"] if next_btn else None
print(all_quotes)







