# eventual ui
# .exe conversion; paste in URL of site? or if we have a set site then just the specific data we want to access
# log in system? or just have it be hosted locally 


# hear me out: user can make files (eg cooking), send beautified scraped notes into that file (eg from cooking websites) for organization

# https://tkdocs.com/
# test from sophia:
from tkinter import *
from tkinter import ttk

from bs4 import BeautifulSoup
import requests

#def calculate(*args):
    #try:
        #value = float(url.get())
        #meters.set(round(0.3048 * value, 4))
    #except ValueError:
        #pass

# later import this function but it is currently winning the battle so it is here now
def scrape(*args):
    try: 
        txt = url.get()
        response = requests.get(str(txt))
        soup = BeautifulSoup(response.text, "html.parser")

    # beautify it
        title = soup.select_one('h1').text
        text = soup.select_one('p').text
        link = soup.select_one('a').get('href')

        print("Title:", title)
        print("Text:", text)
        print("Link:", link)
    
    except ValueError:
        pass


root = Tk()
root.title("URL Scraper")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

url = StringVar()
url_entry = ttk.Entry(mainframe, width=7, textvariable=url)
url_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Button(mainframe, text="Scrape", command=scrape).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="Enter URL").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Result").grid(column=3, row=2, sticky=W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

url_entry.focus()
root.bind("<Return>", scrape)

root.mainloop()