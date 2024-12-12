from tkinter import *
from tkinter import messagebox
from random import *
import pyperclip
import json
FONT_NAME = "Lucida Grande"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(password) == 0 or len(website) == 0:
        messagebox.showinfo(title="Error", message="please ensure fields are not empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                #read old data
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH ------------------------------- #

def search():
    user_input = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            # read old data
            data = json.load(data_file)
            #search data
            if user_input in data:
                email = data[user_input]["email"]
                password = data[user_input]["password"]
                messagebox.showinfo(title=email, message=password)
                pyperclip.copy(password)
            else:
                messagebox.showerror("Error", "No website found")

    except FileNotFoundError:
        messagebox.showerror("Error", "No password have been saved in this database.")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("My PW Manager")
window.config(padx=40, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1,)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

website_entry = Entry(width=21)
website_entry.grid(column=1,row=1, columnspan=2, sticky="EW")
#Cursor Focus
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(column=1,row=2, columnspan=2, sticky="EW")
#auto-populate domain
email_entry.insert(END, "@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(column=1,row=3, sticky="EW")

gen_pw_button = Button( text="Generate Password", command=password_generator)
gen_pw_button.grid(column=2,row=3, sticky="EW")

add_button = Button(width=36, text="Add", command=save)
add_button.grid(column=1,row=4, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=search)
search_button.grid(column=2,row=1, sticky="EW")

window.mainloop()
