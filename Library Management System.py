import sqlite3  # importing module for performing SQL operations.
from tkinter import *  # importing module for creating GUI
from tkinter import messagebox


class DB:  # creating a class DB with functions to perform various operations on the database.
    def __init__(self):  # constructor functor for class DB.
        # connects to a database called mybooks.db
        self.conn = sqlite3.connect("mybooks.db")
        self.cur = self.conn.cursor()  # creating a cursor to navigate through the database
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT)")  # creating a table called book with id, title, author and isbn as columns.
        self.conn.commit()  # commit functions saves everything to the database

    def __del__(self):  # destructor created for the class DB
        self.conn.close()  # closes the connection with the database

    def view(self):  # To view all the rows present in the table
        # Execute function is to perform the SQL operations. Here, it produces all the rows from the table.
        self.cur.execute("SELECT * FROM book")
        # fetching all the rows one by one from the table and storing it in list rows
        rows = self.cur.fetchall()
        return rows

    def insert(self, title, author, isbn):  # inserting a new row in the table.
        # passing values to the function to store them in the columns
        self.cur.execute("INSERT INTO book VALUES (NULL,?,?,?)",
                         (title, author, isbn,))
        self.conn.commit()
        self.view()

    # to update the values of the selected row with the values passed by the user
    def update(self, id, title, author):
        self.cur.execute(
            "UPDATE book SET title=?, author=? WHERE id=?", (title, author, id,))
        self.conn.commit()
        self.view()

    # to delete the row from the table given the value of the id of the selected row.
    def delete(self, id):
        self.cur.execute("DELETE FROM book WHERE id=?", (id,))
        self.conn.commit()
        self.view()

    # to search for a given entry in the table given either the value of the title or author name
    def search(self, title="", author=""):
        self.cur.execute(
            "SELECT * FROM book WHERE title=? OR author=?", (title, author,))
        rows = self.cur.fetchall()
        return rows


# created an object of the class DB. Now database is connected and a new table book has been formed.
db = DB()


def get_selected_row(event):  # selecting a particular row or multiple rows
    global selected_tuple
    index = list1.curselection()[0]  # this is the id of the selected tuple
    selected_tuple = list1.get(index)
    # deleting the value so that can be used again for next book
    e1.delete(0, END)
    e1.insert(END, selected_tuple[1])  # inserting the title of the book
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2])  # inserting author name
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3])  # inserting issue number isbn


def view_command():  # to print all the rows of the table using view function of the class DB on to the screen
    list1.delete(0, END)  # empty the list
    for row in db.view():  # loop until we reach the end of the table book
        list1.insert(END, row)  # keeps on inserting each row into the list


def search_command():  # to print the row we want based on title or author
    list1.delete(0, END)  # empty the list
    # get the name of the title or the author and pass it to the search function of class DB
    for row in db.search(title_text.get(), author_text.get()):
        # will insert all the rows having the same value of title or author
        list1.insert(END, row)


def add_command():  # to add a new row into the table
    db.insert(title_text.get(), author_text.get(),
              isbn_text.get())  # passing user input values
    list1.delete(0, END)  # empty the list
    # insert into the list and then the table, the values given by the user
    list1.insert(END, (title_text.get(), author_text.get(), isbn_text.get()))


def delete_command():  # deleting a row
    # calls the delete function of the class DB and passes the id as the parameter and condition
    db.delete(selected_tuple[0])


def update_command():
    # calls the update function of the class DB and passes the user input as parameters to update value of the row
    db.update(selected_tuple[0], title_text.get(), author_text.get())


window = Tk()  # using Tkinter module, create a GUI window

window.title("My Books")  # setting title of the window


def on_closing():  # destructor for the window
    dd = db
    # when ok is clicked, displays the following message
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        del dd  # deletes the object once window has been closed


window.protocol("WM_DELETE_WINDOW", on_closing)  # handles window closing

l1 = Label(window, text="Title")  # creating input labels in the window
l1.grid(row=0, column=0)  # determining size of the input grid for these labels

l2 = Label(window, text="Author")
l2.grid(row=0, column=2)

l3 = Label(window, text="ISBN")
l3.grid(row=1, column=0)

title_text = StringVar()
# taking input from the user in the grid and storing it in a string variable
e1 = Entry(window, textvariable=title_text)
e1.grid(row=0, column=1)

author_text = StringVar()  # taking author name input
e2 = Entry(window, textvariable=author_text)
e2.grid(row=0, column=3)

isbn_text = StringVar()  # taking isbn input
e3 = Entry(window, textvariable=isbn_text)
e3.grid(row=1, column=1)

# creating the list space to display all the rows of the table
list1 = Listbox(window, height=25, width=65)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)  # determining the size

# creating a scrollbar for the window to scroll through the list entries
sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

# configuring the scroll function for the scrollbar object sb1
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

# creating buttons for the various operations. Giving it a name and assigning a particular command to it.
b1 = Button(window, text="View all", width=12, command=view_command)
b1.grid(row=2, column=3)  # size of the button

b2 = Button(window, text="Search entry", width=12, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Add entry", width=12, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Update selected", width=12, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Delete selected", width=12, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=7, column=3)

# carry the functioning of the GUI window on a loop until it is closed using the destructor
window.mainloop()