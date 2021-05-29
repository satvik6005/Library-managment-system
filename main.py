from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from os.path import isfile
import sqlite3

# database class
class db():
    #check weather database exis or not
    def __init__(self):
        if isfile('database.db') == True:
            pass
        else:
            messagebox.showinfo('info', 'databse does not exist creating')
            self.create()

    def create(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute(""" CREATE table books(
        book_id Integer Primary Key,
        name text,
        author text,
        genre text,
        user integer
        )""")
        cur.execute(""" CREATE table users(
        user_id Integer Primary Key,
        name text,
        book integer
        )""")
        conn.commit()
        conn.close()

    def add_user(self, name, id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('Insert into users(user_id,name) VALUES (?,?)', (id, name))
        conn.commit()
        cur.execute('select * FROM users')

    def add_book(self, name, id, genre, author):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('Insert into books (book_id,name,author,genre) VALUES(?,?,?,?)', (id, name, author, genre))
        conn.commit()
        cur.execute('select * FROM books')
        conn.close()

    def add_issue(self, userid, bookid):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('UPDATE users set book=(?)', (bookid,))
        cur.execute('UPDATE books set user=(?)', (userid,))
        conn.commit()
        cur.execute('select * FROM books')
        conn.close()

    def check_user_exist(self, id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('select user_id from users where user_id=(?)', (id,))
        if cur.fetchone() is None:
            conn.close()
            return False
        else:
            conn.close()
            return True

    def check_book_exist(self, id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('select book_id from books where book_id=(?)', (id))
        if cur.fetchone() is None:
            conn.close()
            return False
        else:
            conn.close()
            return True

    def check_book_issued(self, id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('select user from books where book_id=(?)', (id,))
        t = cur.fetchone()
        if t[0] is None:
            conn.close()

            return False
        else:
            conn.close()

            return True

    def check_user_has_book(self, id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('select book from users where user_id=(?)', (id,))
        t = cur.fetchone()
        if t[0] is None:
            conn.close()
            return False
        else:
            conn.close()
            return True

    def create_list_of_books(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('select book_id,name,author,genre from books')
        t = cur.fetchall()
        conn.close()
        return t
    # search book in database
    def searc(self, name):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('select book_id,name,author,genre from books where name   Like (?)', ('%' + name + '%',))
        print('\'' + '%' + name + '%' + '\'')
        t = cur.fetchall()
        conn.close()
        return t

#main window class
class Main_Window(Tk):

    def __init__(self):
        self.root = super().__init__()
        self.label = Label()
        #images used in the programme
        self.im1 = ImageTk.PhotoImage(Image.open("images.png").resize((800, 150)))
        self.im2 = ImageTk.PhotoImage(Image.open("b.png").resize((70, 50)))
        self.im3 = ImageTk.PhotoImage(Image.open("user.png").resize((70, 50)))
        self.im4 = ImageTk.PhotoImage(Image.open("issue.png").resize((70, 50)))
        self.im5 = ImageTk.PhotoImage(Image.open('hom.png').resize((30, 30)))
        self.database = db()
        #frames defined in programme
        self.frame = Frame(self.root, height=120, bd=7, relief=SUNKEN)

        self.frame.pack(fill=X)

        self.labim = Label(self.frame, image=self.im1)
        self.labim.pack()
        self.frame2 = Frame(self.root, height=100, relief=SUNKEN, bd=7, bg='light green')
        self.frame2.pack(fill=X)
        self.frame3 = Frame(self.root, height=450, relief=SUNKEN, bd=7, bg='light blue')
        self.frame3.pack(fill=BOTH)
        self.frame4 = Frame(self.frame2, width=500, height=100, bd=7, bg='light green')
        self.frame4.grid(row=0, column=0)
        self.frame5 = Frame(self.frame2, width=300, height=100, relief=SUNKEN, bd=2, bg='light green')
        self.frame5.grid(row=0, column=1)
        #buttons and entry used programmes
        self.button1 = Button(self.frame4, text='ADD BOOK', height=70, width=140, image=self.im2, compound='left',
                              command=self.book)
        self.button1.place(x=25, y=5)
        self.button2 = Button(self.frame4, text='ADD USER', height=70, width=140, image=self.im3, compound='left',
                              command=self.user)
        self.button2.place(x=180, y=5)
        self.button3 = Button(self.frame4, text='ISSUE BOOK', height=70, width=140, image=self.im4, compound='left',
                              command=self.issue)
        self.button3.place(x=340, y=5)
        self.list1 = Listbox(self.frame3, width=40, height=450, selectmode=SINGLE, font=('Cooper', 10, 'bold'))
        self.scroll = Scrollbar(self.frame3, orient=VERTICAL)
        self.list2 = Listbox(self.frame3, width=40, height=450, font=('Cooper', 10, 'bold'))
        self.list3 = Listbox(self.frame3, width=40, height=450, font=('Cooper', 10, 'bold'))

        self.list1.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.list1.yview)
        self.list3.pack(side=RIGHT, fill=Y)
        self.name_label = Label(self.frame3, text="User Name:", font=('Cooper', 18), bg='#ED6B00')
        self.roll_label = Label(self.frame3, text="Roll no:", font=('Cooper', 18), bg='#ED6B00')
        self.entry1 = Entry(self.frame3)
        self.entry2 = Entry(self.frame3)
        self.button4 = Button(self.frame3, text='Submit', command=self.user_add)
        self.name_book = Label(self.frame3, text="Title:", font=('Cooper', 18), bg='#ED6B00')
        self.book_id = Label(self.frame3, text="ID:", font=('Cooper', 18), bg='#ED6B00')
        self.entry3 = Entry(self.frame3)
        self.entry4 = Entry(self.frame3)
        self.genre = Label(self.frame3, text="Genre:", font=('Cooper', 18), bg='#ED6B00')
        self.author = Label(self.frame3, text="Author:", font=('Cooper', 18), bg='#ED6B00')
        self.entry5 = Entry(self.frame3)
        self.entry6 = Entry(self.frame3)
        self.button5 = Button(self.frame3, text='submit', command=self.book_add)
        self.issue_userid = Label(self.frame3, text="User id:", font=('Cooper', 18), bg='#ED6B00')
        self.issue_bookid = Label(self.frame3, text="book id:", font=('Cooper', 18), bg='#ED6B00')
        self.entry7 = Entry(self.frame3)
        self.entry8 = Entry(self.frame3)
        self.button6 = Button(self.frame3, text='submit', command=self.issue_add)
        self.entry9 = Entry(self.frame5, width=46)
        self.entry9.grid(row=0, column=0)
        self.button7 = Button(self.frame5, text='search', height=3, width=38, font=("Comic Sans Ms", 8),
                              command=self.search)
        self.button7.grid(row=1, column=0)
        self.home_label = Label(self.frame3, image=self.im5)
        self.home_label.bind("<Button-1>", lambda event: self.initial_window())
        self.books = self.database.create_list_of_books()
        self.list1.bind('<Double-Button-1>', lambda event: self.ok(1))
        self.list3.bind('<Double-Button-1>', lambda event: self.ok(2))
        self.searchcache=[]
        self.entry9.bind('<Return>',lambda event: self.search())


        self.initial_window()

    def search(self):
        lis = self.database.searc(self.entry9.get())
        self.list3.delete(0, END)
        self.searchcache=[]
        for i in range(0, len(lis)):
            self.list3.insert(i, lis[i][1])
            self.searchcache.append(lis[i])
    #show book status function in list2
    def ok(self, i):
        self.list2.delete(0, END)
        lis = ['book id', 'book name', 'Author', "Genre"] #list of contents to show

        if i == 1:
            index = self.list1.curselection()
            self.list2.insert(0, "book id  {}".format(self.books[index[0]][0]))
            for i in range(1, 4):
                self.list2.insert(i, lis[i] + "  " + self.books[index[0]][i])
        else:
            if self.searchcache is None:
                return
            else:
                index = self.list3.curselection()


                for i in range(0,len(self.books)):
                    if self.searchcache[index[0]][0]==self.books[i][0]:
                        self.list2.delete(0,END)
                        self.list2.insert(0, "book id  {}".format(self.books[i][0]))
                        for j in range(1, 4):
                            self.list2.insert(j, lis[j] + "  " + self.books[i][j])




    def issue(self):
        self.user_forget()
        self.book_forget()
        self.initial_window_forget()
        self.frame3.config(bg='#ED6B00')
        self.home_label.place(x=2)

        self.issue_userid.place(x=50, y=50)
        self.entry7.place(x=150, y=60)
        self.issue_bookid.place(x=50, y=100)
        self.entry8.place(x=150, y=110)
        self.button6.place(x=100, y=160)

    def issue_forget(self):
        self.issue_userid.place_forget()
        self.entry7.place_forget()
        self.issue_bookid.place_forget()
        self.entry8.place_forget()
        self.button6.place_forget()
        self.home_label.place_forget()

    def initial_window(self):
        self.user_forget()
        self.book_forget()
        self.issue_forget()
        self.list1.pack(side=LEFT, fill=Y)
        self.scroll.pack(side=LEFT, fill=Y)
        self.list2.pack(side=LEFT, fill=Y)
        self.list1.delete(0, END)
        for i in self.books:
            self.list1.insert(END, i[1])

    def initial_window_forget(self):
        self.list1.pack_forget()
        self.scroll.pack_forget()
        self.list2.pack_forget()

    def user(self):
        self.initial_window_forget()
        self.book_forget()
        self.issue_forget()
        self.frame3.config(bg='#ED6B00')
        self.home_label.place(x=2)

        self.name_label.place(y=50, x=50)
        self.roll_label.place(y=100, x=50)
        self.entry1.place(y=55, x=210)
        self.entry2.place(y=110, x=210)
        self.button4.place(y=200, x=180)

    def user_forget(self):
        self.name_label.place_forget()
        self.roll_label.place_forget()
        self.entry1.place_forget()
        self.entry2.place_forget()
        self.button4.place_forget()
        self.home_label.place_forget()

    def book(self):
        self.initial_window_forget()
        self.user_forget()
        self.issue_forget()
        self.frame3.config(bg='#ED6B00')
        self.home_label.place(x=2)
        self.name_book.place(y=50, x=50)
        self.book_id.place(y=100, x=50)
        self.entry3.place(y=55, x=210)
        self.entry4.place(y=110, x=210)
        self.genre.place(y=150, x=50)
        self.author.place(y=200, x=50)
        self.entry5.place(x=210, y=160)
        self.entry6.place(x=210, y=200)
        self.button5.place(x=250, y=250)

    def book_add(self):
        if self.entry3.get() == "" or self.entry4.get() == "" or self.entry5.get() == "" or self.entry6.get() == "":
            messagebox.showerror('error', 'fill all entry box')
        elif not self.entry4.get().isnumeric():
            messagebox.showerror('error', 'id must be integer')
        else:
            self.database.add_book(self.entry3.get(), self.entry4.get(), self.entry5.get(), self.entry6.get())
            self.books.append((self.entry4.get(),self.entry3.get() ,self.entry6.get(), self.entry5.get())) #update books cache
            messagebox.showinfo('info', 'book added')

    def user_add(self):
        if self.entry1.get() == "" or self.entry2.get() == "":
            messagebox.showerror('error', 'fill all entry box')
        elif not self.entry2.get().isnumeric():
            messagebox.showerror('error', 'id must be integer')
        else:
            self.database.add_user(self.entry1.get(), self.entry2.get())
            messagebox.showinfo('info', 'user added')

    def issue_add(self):
        if self.entry7.get() == "" or self.entry8.get() == "":
            messagebox.showerror('error', 'fill all entry box')
        elif not self.entry7.get().isnumeric():
            messagebox.showerror('error', 'user id must be integer')
        elif not self.entry8.get().isnumeric():
            messagebox.showerror('error', 'book id must be integer')

        elif self.database.check_user_exist(self.entry7.get()) is False:
            messagebox.showerror('error', 'user does''t exist')
        elif self.database.check_book_exist(self.entry8.get()) is False:
            messagebox.showerror('error', 'book does not exist')
        elif self.database.check_book_issued(self.entry8.get()) is True:
            messagebox.showerror('error', 'book is already issued')
        elif self.database.check_user_has_book(self.entry7.get()) is True:
            messagebox.showerror('error', 'user hase book cannot issue anymore')
        else:
            self.database.add_issue(self.entry7.get(), self.entry8.get())
            messagebox.showinfo('info', 'book issued')

    def book_forget(self):
        self.name_book.place_forget()
        self.book_id.place_forget()
        self.entry3.place_forget()
        self.entry4.place_forget()
        self.genre.place_forget()
        self.author.place_forget()
        self.entry5.place_forget()
        self.entry6.place_forget()
        self.button5.place_forget()
        self.home_label.place_forget()


ojb = Main_Window()
ojb.geometry('800x700')
ojb.title('Library')
ojb.resizable(False, False)
ojb.mainloop()
