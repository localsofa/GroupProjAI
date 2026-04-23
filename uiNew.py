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

        # extract title
        title_elem = soup.find('h1') or soup.find('title')
        title = title_elem.text.strip() if title_elem else "No title found"

        # find main content area
        main_content = (soup.find('article') or 
                       soup.find('main') or 
                       soup.find('div', class_=lambda x: x and ('content' in x.lower() or 'post' in x.lower() or 'entry' in x.lower())) or
                       soup.find('div', id=lambda x: x and ('content' in x.lower() or 'post' in x.lower() or 'main' in x.lower())) or
                       soup.body)

        if main_content:
            # extract paragraphs (filter out short ones like nav)
            paragraphs = [p.get_text(strip=True) for p in main_content.find_all('p') if len(p.get_text(strip=True)) > 50]
            # extract lists
            lists = [li.get_text(strip=True) for li in main_content.find_all('li') if len(li.get_text(strip=True)) > 5]
        else:
            paragraphs = []
            lists = []

        # print results
        print("Title:", title)
        print("\nMain Text:")
        for para in paragraphs[:5]:  # limit to first 5
            print(para[:200] + "..." if len(para) > 200 else para)
        print("\nLists:")
        for item in lists[:10]:  # limit
            print("-", item)

        # save to file
        filename = f"{title.replace('/', '_').replace(' ', '_').replace(':', '_')[:50]}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n\nMain Text:\n")
            for para in paragraphs:
                f.write(para + "\n\n")
            f.write("\nLists:\n")
            for item in lists:
                f.write(f"- {item}\n")
        print(f"\nSaved to {filename}")
    
    except Exception as e:
        print("Error:", str(e))
    
    except Exception as e:
        print("Error:", str(e))


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