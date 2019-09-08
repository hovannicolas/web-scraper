import requests
from bs4 import BeautifulSoup
from csv import writer
from random import choice

BASE_URL = "http://quotes.toscrape.com"


# web-scraping logic
def scrape_quotes():
    all_quotes = []
    url = "/page/1"
    while url:
        response = requests.get(f"{BASE_URL}{url}")
        print(f"Now scraping {BASE_URL}{url}...")
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
    return all_quotes


# game logic
def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    guess = " "
    print("Let's play a game! Here is a quote: ")
    print(quote["text"])
    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses} \n")
        if guess.lower() == quote["author"].lower():
            print("Correct, you won!")
            break
        print("Incorrect!! Here's a hint..")
        remaining_guesses -= 1
        if remaining_guesses == 3:
            response = requests.get(f"{BASE_URL}{quote['bio-href']}")
            soup = BeautifulSoup(response.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(f"This author was born on {birth_date} {birth_place}")
        elif remaining_guesses == 2:
            print(f"The author's name starts with the letter: {quote['author'][0]}")
        elif remaining_guesses == 1:
            print(f"The author's last name starts with the letter: {quote['author'].split(' ')[1][0]}")
        else:
            print(f"Game over, you ran out of guesses!! The answer was: {quote['author']}")
    # replay logic
    again = ' '
    while again not in ['yes', 'y', 'no', 'n']:
        again = input("Would you like to play again? (y/n) \n")
    if again in ['yes', 'y']:
        print("Affirmative, starting the game over..")
        start_game(quotes)
    else:
        print("See ya later! Thanks for playing.")


quotes = scrape_quotes()
start_game(quotes)
