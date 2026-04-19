# PREQUESITES:
# pip install requests
# pip install beautifulsoup4
# pip install beautifulsoup --> sometimes it's weird abt importing beautifulsoup4 lol


# webscraper
# request handler
# keyword finder? 
# pandas! maybe analystics or visualization?

import requests
from bs4 import BeautifulSoup

# take URL input from user eg & scrape it yay: 

def scrape(txt):
    
    #url = input("Enter URL: ")
    url = txt
    response = requests.get(str(url))
    soup = BeautifulSoup(response.text, "html.parser")

    # beautify it
    title = soup.select_one('h1').text
    text = soup.select_one('p').text
    link = soup.select_one('a').get('href')

    print("Title:", title)
    print("Text:", text)
    print("Link:", link)

scrape()
# scrape() if button clicked in ui
# EXAMPLE USAGE: past https://www.scrapethissite.com/pages/simple/
# current only works on simple sites like that one
# ollama usage for the topicalization? or keyword search 


# later - take info, create subtopics, save under some sort of title if user has requested it in UI - prob an if else
# store in Streamlit Community Cloud? 