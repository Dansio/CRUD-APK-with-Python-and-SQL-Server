from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W, E, N, S, END
from tkinter import ttk
from tkinter import messagebox
import sys
from database_config import dbConfig
import psycopg2
import time as t

#connection to the database
con = psycopg2.connect(**dbConfig)
print(con)

#create cursor
cursor = con.cursor()


class Bookdb:
    def __init__(self):
        self.con = psycopg2.connect(**dbConfig)
        self.cursor = con.cursor()
        print("You have connected to the database")
        print(con)


    def __del__(self):
        self.con.close()

    def view (self):
        self.cursor.execute("SELECT * FROM books")
        row = self.cursor.fetchall()
        return row

    def insert (self, title, author, isbn):
        sql=("INSERT INTO books(title,author,isbn)VALUES (%s,%s,%s)")
        values = [title, author, isbn]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title = "Book Database", message = "New Books added to Database")

    def update(self, id, title, author, isbn):
        pgsql = 'UPDATE books SET title = %s, author = %s, isbn = %s WHERE id = %s'
        self.cursor.execute(pgsql, [title, author,isbn,id])
        self.con.commit()
        messagebox.showinfo(title = "Book Database", message = "Book Updated")


    def delete(self, id):
        delquery ='DELETE FROM books WHERE id = %s'
        self.cursor.execute(delquery, [id])
        self.con.commit()
        messagebox.showinfo(title="Book Database",message="Book Deleted")

db = Bookdb()


def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    title_entry.delete(0, 'end')
    title_entry.insert('end', selected_tuple[1])
    author_entry.delete(0, 'end')
    author_entry.insert('end', selected_tuple[2])
    isbn_entry.delete(0, 'end')
    isbn_entry.insert('end', selected_tuple[3])

# create view Function
def view_records():
    list_bx.delete(0, 'end')
    for row in db.view():
        list_bx.insert('end', row)

#function to add new book

def add_book():
    db.insert(title_text.get(),author_text.get(),isbn_text.get())
    list_bx.delete(0, 'end')
    list_bx.insert('end', (title_text.get(), author_text.get(), isbn_text.get()))
    title_entry.delete(0, "end") # Clears input after inserting
    author_entry.delete(0, "end")
    isbn_entry.delete(0, "end")
    con.commit()

#delete records
def delete_records():
    db.delete(selected_tuple[0])
    con.commit()

#function to clear the Screen
def clear_screen():
    list_bx.delete(0,'end')
    title_entry.delete(0,'end')
    author_entry.delete(0,'end')
    isbn_entry.delete(0,'end')

#function to update selected records
def update_records():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
    title_entry.delete(0, "end") # Clears input after inserting
    author_entry.delete(0, "end")
    isbn_entry.delete(0, "end")
    con.commit()

#ask you a message if you tried to close the apk from another button than the exit button
def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        del dd


#main variable, create applications window
root = Tk()


#Create APK window, define the background colour and geometry
root.title("My Books Database Application")
root.configure(background = "light grey")
root.geometry("1000x500")
root.resizable(width=False,height=False)

#Create Title input box
title_label = ttk.Label(root, text='Title', background = 'light grey', font=("tkDefaultFont",16))
title_label.grid(row = 0, column = 0, sticky = W)
title_text = StringVar()
title_entry = ttk.Entry(root, width=24, textvariable = title_text)
title_entry.grid(row = 0, column = 1, sticky=W)

#Create Author input box
author_label = ttk.Label(root, text='Author', background = 'light grey', font=("tkDefaultFont",16))
author_label.grid(row = 0, column = 2, sticky = W)
author_text = StringVar()
author_entry = ttk.Entry(root, width=24, textvariable = author_text)
author_entry.grid(row = 0, column = 3, sticky=W)

#Create ISBN input box
isbn_label = ttk.Label(root, text='ISBN', background = 'light grey', font=("tkDefaultFont",16))
isbn_label.grid(row = 0, column = 4, sticky = W)
isbn_text = StringVar()
isbn_entry = ttk.Entry(root, width=24, textvariable = isbn_text)
isbn_entry.grid(row = 0, column = 5, sticky=W)

#Create the Add Book Button
add_btn = Button(root, text="Add Book", bg="blue", fg="white", font ="helvetica 10 bold", command = add_book)
add_btn.grid(row=0, column=6, sticky=W)

# Add  a listbox  to display data from database
# padx and pady method is used to add space (margin) horizontally and vertically
list_bx = Listbox(root, height=16, width=40, font='helvetica 13', bg ='light blue')
list_bx.grid(row=3,column=1, columnspan=14,sticky=W + E,pady=40,padx=15)
list_bx.bind('<<ListboxSelect>>',get_selected_row)

#Create a scroll bar
scroll_bar = Scrollbar(root)
scroll_bar.grid(row = 1, column = 8, rowspan = 14, sticky=W)
#Attach the scrollbar into the listbox (yscroll bar for vertical scrollbar)
list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command = list_bx.yview)

#create a Modify button
modify_btn = Button(root, text= "Modify Record",bg='purple', fg = "white", font ="helvetica 10 bold", command = update_records)
modify_btn.grid(row=15, column=4)

#create a Delete button
delete_btn = Button(root, text= "Delete Record",bg='red', fg = "white", font ="helvetica 10 bold", command = delete_records)
delete_btn.grid(row=15, column=5)

#create a View button
view_btn = Button(root, text= "View Record",bg='black', fg = "white", font ="helvetica 10 bold", command =view_records)
view_btn.grid(row=15, column=1)

#create a Clear Screen button
clear_btn = Button(root, text= "Clear Screen",bg='maroon', fg = "white", font ="helvetica 10 bold", command =clear_screen)
clear_btn.grid(row=15, column=2)

#create a Exit button
exit_btn = Button(root, text= "Exit Application",bg='blue', fg = "white", font ="helvetica 10 bold", command = root.destroy)
exit_btn.grid(row=15, column=3)


#function to loop the apk
root.mainloop()
