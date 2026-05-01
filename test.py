
# ------ SETUP ------ 
# only for non .exe file
# create venv
# pip install beautifulsoup4 requests os

# ------ IMPORTS ------ 
#from tkinter import *
#from tkinter import ttk
#from tkinter import filedialog, simpledialog
from customtkinter import *
from customtkinter import filedialog 
import customtkinter as ctk 
import os

from bs4 import BeautifulSoup
import requests

# ------  HELPER FUNCTIONS ------
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

        # save to file if user checked off box
        if save_file.get():
            os.makedirs(save_dir.get(), exist_ok=True)
            filename = f"{title.replace('/', '_').replace(' ', '_').replace(':', '_')[:50]}.txt"
            filepath = os.path.join(save_dir.get(), filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n\nMain Text:\n")
                for para in paragraphs:
                    f.write(para + "\n\n")
                f.write("\nLists:\n")
                for item in lists:
                    f.write(f"- {item}\n")
            print(f"\nSaved to {filepath}")
    
    except Exception as e:
        print("Error:", str(e))


# choose directory for saving files
def choose_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        save_dir.set(dir_path)


# option to create folder
def create_folder():
    name = ctk.CTkInputDialog("Create Folder", "Enter folder name:")
    if name:
        folder_path = os.path.join(save_dir.get(), name)
        os.makedirs(folder_path, exist_ok=True)
        save_dir.set(folder_path)


# ------ UI ------ 
root = CTk()
root.title("URL Scraper")

mainframe = ctk.CTkFrame(master=root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

set_appearance_mode("dark") 

url = StringVar()
save_file = BooleanVar()
save_dir = StringVar(value="scraped_files")
url_entry = ctk.CTkEntry(mainframe, width=7, textvariable=url)
url_entry.grid(column=3, row=1, sticky=(W, E))

ctk.CTkButton(mainframe, text="Scrape", command=scrape, corner_radius=32, fg_color="#457a00",
                hover_color="#b175ff", border_color="#ffffff",
                border_width=2).grid(column=3, row=3, sticky=W)

ctk.CTkCheckBox(mainframe, text="Save to file", variable=save_file).grid(column=4, row=5, sticky=W)

ctk.CTkLabel(mainframe, text="Save Folder:").grid(column=1, row=5, sticky=W)
save_dir_entry = ctk.CTkEntry(mainframe, textvariable=save_dir)
save_dir_entry.grid(column=2, row=5, columnspan=2, sticky=(W, E))
ctk.CTkButton(mainframe, text="Browse", command=choose_dir, corner_radius=32, fg_color="#457a00",
                hover_color="#b175ff", border_color="#ffffff",
                border_width=2).grid(column=3, row=6, sticky=W)
ctk.CTkButton(mainframe, text="Create Folder", command=create_folder, corner_radius=32, fg_color="#457a00",
                hover_color="#b175ff", border_color="#ffffff",
                border_width=2).grid(column=4, row=6, sticky=W)

ctk.CTkLabel(mainframe, text="Enter URL").grid(column=4, row=1, sticky=W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

url_entry.focus()
root.bind("<Return>", scrape)

root.mainloop()