# ------ SETUP ------ 
# only for non .exe file
# create venv
# pip install beautifulsoup4 requests os
# possible thing for sentiment analysis: https://github.com/shabisht/Sentiment-Analysis-API

# ------ IMPORTS ------ 
#from tkinter import *
#from tkinter import ttk
#from tkinter import filedialog, simpledialog
from customtkinter import *
from customtkinter import filedialog
import customtkinter as ctk
import os
import ollama

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

        # summarize scraped text with Ollama
        full_text = "\n".join(paragraphs[:10]) # limit context given to Ollama
        if full_text:
            print("\nSummarizing...")
            summary = summarize(full_text)
            print("\nSummary:", summary)
            # push summary into text widget
            result_text.configure(state = NORMAL)
            result_text.delete(1.0, END)
            result_text.insert(END, f"Title: {title}\n\nSummary:\n{summary}")
            result_text.configure(state = DISABLED)
            
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

# summarize URL
def summarize(text):
    try:
        response = ollama.chat(
            model = "llama3.2:1b",
            messages = [{
                "role": "user",
                "content": f"Summarize the following text:\n\n{text}"
            }]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Summarization error: {str(e)}"

# ------ UI ------ 
root = CTk()
root.title("URL Scraper")

mainframe = ctk.CTkFrame(root)
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

ctk.CTkCheckBox(mainframe, text="Save to file", variable=save_file).grid(column=3, row=4, sticky=W)

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

# Text widget
result_text = ctk.CTkTextbox(mainframe, height = 300, width = 60, wrap = WORD, state = DISABLED)
result_text.grid(column = 1, row = 7, columnspan = 5, rowspan = 10, sticky = (W, E), pady = 10)
scrollbar = ctk.CTkScrollbar(mainframe, orientation = VERTICAL, command = result_text.yview)
scrollbar.grid(column = 7, row = 7, sticky = (N, S))
result_text.configure(yscrollcommand = scrollbar.set)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

url_entry.focus()
root.bind("<Return>", scrape)

root.mainloop()