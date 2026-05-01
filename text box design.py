from customtkinter import *

app = CTk()
app.geometry("400x200")

set_appearance_mode("dark")

btn = CTkButton(master=app, text="Scrape", corner_radius=32, fg_color="#457a00",
                hover_color="#b175ff", border_color="#ffffff",
                border_width=2)


btn.place(relx=0.5, rely=0.25, anchor= "center")

switch = CTkSwitch(master=app, text="Option")

switch.place(relx=0.5, rely=0.5, anchor="center")

entry = CTkEntry(master=app, placeholder_text="URL:", width=300,
                 text_color="#ffffff")

entry.place(relx=0.5, rely=0.75, anchor="center")

app.mainloop()