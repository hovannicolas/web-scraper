import requests
from bs4 import BeautifulSoup
from csv import writer
from random import choice

all_quotes =[]
base_url = "http://quotes.toscrape.com"
url = "/page/1"

# web-scraping logic
while url:
    response = requests.get(f"{base_url}{url}")
    print(f"Now scraping {base_url}{url}...")
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = (soup.find_all(class_="quote"))

    for quote in quotes:
        all_quotes.append({
        "text": quote.find(class_="text").get_text(),
        "author": quote.find(class_="author").get_text(),
        "bio-href": quote.find("a")["href"]
        })
    next_btn = soup.find(class_="next")
    url = next_btn.find("a")["href"] if next_btn else None

# game logic
quote = choice(all_quotes)
remaining_gusses = 4
guess = " "
print("Let's play a game! Here is a quote: ")
print(quote["text"])


while guess.lower() != quote["author"].lower() and remaining_gusses > 0:
    guess = input(f"Who said this quote? Guesses remaining: {remaining_gusses} \n")
    if guess.lower() == quote["author"].lower():
        print("Correct, you won!")
        break
    print("Incorrect!! Here's a hint..")
    remaining_gusses -= 1
    if remaining_gusses == 3:
        response = requests.get(f"{base_url}{quote['bio-href']}")
        soup = BeautifulSoup(response.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(f"This author was born on {birth_date} {birth_place}")
    elif remaining_gusses == 2:
        print(f"The author's name starts with the letter: {quote['author'][0]}")
    elif remaining_gusses == 1:
        print(f"The author's last name starts with the letter: {quote['author'].split(' ')[1][0]}")
    else:
        print(f"Game over, you ran out of guesses!! The answer was: {quote['author']}")










