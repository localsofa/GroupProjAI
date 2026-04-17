# PREQUESITES:
# pip install requests
# pip install beautifulsoup4


# webscraper
# request handler
# keyword finder? 
# pandas! maybe analystics or visualization?

import requests
from bs4 import BeautifulSoup

# take URL input from user eg & do things yay: 

def scrape():
    
    url = input("Enter URL: ")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)

# scrape()
# later - take info, create subtopics, save under some sort of title if user has requested it in UI