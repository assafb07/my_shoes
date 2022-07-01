import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

db = 'my_shoes.db'
bg02 = '#403e78'
bg01 = "#78a4f5"

connection = sqlite3.connect('My_Shoes.db')
cursor = connection.cursor()
try:
    connection.execute("""CREATE TABLE Shoes (
            id int, AUTO_INCREMENT,
            brand text,
            model text,
            color text,
            ks REAL

            )""")
except: print ('table exist. Move on')

class Shoes:
    def __init__(self, id, brand, model, color, ks):
        self.id = id
        self.brand = brand
        self.model = model
        self.color = color
        self.ks = ks

    def make_shoe_name(self,id):
            connection = sqlite3.connect(db)
            cursor = connection.cursor()
            sql = 'SELECT brand and model and color FROM shoes WHERE id=?'
            val = ( self.id )
            with connection:
                cursor.execute(sql,val)
                found_the_shoe = cursor.fetchone()
                shoe_name = found_the_shoe[0] + ' ' + found_the_shoe[1] + ' ' + found_the_shoe[2]
                return (shoe_name)
            connection.close()
    def Add_Shoe_Sql(self,brand,model,color):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        sql = 'INSERT INTO Shoes(brand, model, color, ks) VALUES (?, ?, ?, ?)'
        val = ( self.brand , self.model , self.color, 0 )

        with connection:
            cursor.execute(sql,val)
        connection.close()
        Load_Frame02()

    def Remove_Shoe_Sql(self,id):

        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        sql = 'DELETE FROM Shoes WHERE id = ?'
        val = (self.id,)

        with connection:
            cursor.execute(sql,val)
        connection.close()
        Load_Frame02()

    def find_ks_for_shoe(self,id,ks):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        sql = 'SELECT ks FROM Shoes WHERE id = ?'
        val = ( self.id )
        with connection:
            cursor.execute(sql,val)
            ks = cursor.fetchone()
        connection.close()

        return (ks)


    def add_ks_to_shoe(self,id,ks):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        sql = 'UPDATE Shoes SET ks = ? WHERE id = ?'
        val = ( self.ks, self.id )
        with connection:
            cursor.execute(sql,val)
        connection.close()
def is_shoe_exist(id):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = ("SELECT * FROM shoes WHERE id = ?")
    val = (id,)
    cursor.execute (sql, val)
    shoe_exist = cursor.fetchall()

    connection.close()
    return shoe_exist

#find all shoes in the DB and make a list all_shoes
def fetch_db():
    all_sheos = 0
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM shoes")
    all_sheos = cursor.fetchall()
    connection.close()
    return all_sheos

#make a nice shoes list with ks
def pre_process(all_sheos):
    shoe_list = []
    for i in all_sheos:
        id = str(i[0])
        brand = i[1]
        model = i[2]
        color = i[3]
        ks = str(i[4])
        shoe_list.append(id + ':' + brand + ' ' + model+ ' ' + color + ':  ' + ks +'Km')
    return shoe_list

def sort_id():


    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    #all ids in table
    sql = 'SELECT id FROM shoes'
    with connection:
        cursor.execute(sql)
        all_id = cursor.fetchall()
    #number of raws(ids)
    sql = 'SELECT COUNT(*) FROM shoes'
    with connection:
        cursor.execute(sql)
        raw_count = cursor.fetchall()
    raw_count_l = (raw_count[0])[0]



    for r in range(0,raw_count_l):
        print ('r=',r)
        find_raw = raw_count_l - r
        this_id = (all_id[find_raw-1])[0]
        new_id = raw_count_l - r
        try:
            sql = 'UPDATE shoes SET id = ? WHERE id = ?'
            val = (new_id,this_id)
            with connection:
                cursor.execute(sql,val)
        except:continue
        connection.close()


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def remove_white_space(from_entry):
    lower_list = from_entry.lower()
    result = [x.replace(' ','') for x in lower_list]
    no_spaces = ''.join(result)
    return no_spaces

def first_character_upper(a_clean):
    lower = a_clean.lower()
    first_upper = lower.capitalize()
    return first_upper

def get_entry_frame03(brand,model,color):
    a = brand.get()
    a_clean = remove_white_space(a)
    a_first_upper = first_character_upper(a_clean)
    b = model.get()
    b_clean = remove_white_space(b)
    b_first_upper = first_character_upper(b_clean)
    c = color.get()
    c_clean = remove_white_space(c)
    c_first_upper = first_character_upper(c_clean)
    e = 0
    d = ''
    new_shoe = Shoes(d,a_first_upper,b_first_upper,c_first_upper,e)
    new_shoe.Add_Shoe_Sql(a,b,c)

def get_entry_frame04(id):
    a = ''
    b = ''
    c = ''
    e = 0
    d = str(id.get())

    delete_shoe = Shoes(d,a,b,c,e)
    delete_shoe.Remove_Shoe_Sql(d)


def get_entry_frame05(id,new_ks):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    shoe_exist = ''
    a=''
    b=''
    c=''
    d = id.get()
    e = new_ks.get()
    print ('here',type(e), e)
    shoe = is_shoe_exist(d)

    if shoe == []:
        not_in_th_list = 'shoe is not in the list'
    else:
        sql = 'SELECT ks FROM Shoes WHERE id = ?'
        val = ( d )
        with connection:
            cursor.execute(sql,val)
            ks = cursor.fetchone()
            try:
                int_e = float(e)
                print (int_e)
                update_ks = int_e+(ks[0])
                add_ks = Shoes(d,a,b,c,update_ks)
                add_ks.add_ks_to_shoe(d,update_ks)
            except:
                print ('not a number')


    Load_Frame02()


#Frame 01
def Load_Frame01():
    bg01 = "#78a4f5"
    frame01.tkraise()
    frame01.pack_propagate(False)
    logo_image = ImageTk.PhotoImage(file = "shoelogo.png")
    logo_widget = tk.Label(frame01, image=logo_image, bg=bg01)
    logo_widget.image = logo_image
    logo_widget.pack(pady=15)
    sort_id()
    tk.Label(frame01,
            text = "How much is enough  :)",
            bg = bg01,
            fg="black",
            font=("TkMenuFont", 17)).pack(pady=15)

    tk.Button(frame01,text="Lets Go!!",
                font=("TkHeadingFont", 20),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:Load_Frame02()).pack(pady=4)

    logo_image = ImageTk.PhotoImage(file = "bottom_image.png")
    logo_widget = tk.Label(frame01, image=logo_image, bg=bg01)
    logo_widget.image = logo_image
    logo_widget.pack()

def Load_Frame02():
    sort_id()
    clear_widgets(frame01)
    clear_widgets(frame02)
    clear_widgets(frame03)
    clear_widgets(frame04)
    frame02.tkraise()
    frame02.pack_propagate(False)
    all_sheos = fetch_db()
    shoe_list = pre_process(all_sheos)
    logo_image = ImageTk.PhotoImage(file = "PngItem_269676.png")
    logo_widget = tk.Label(frame02, image=logo_image, bg=bg01)
    logo_widget.image = logo_image
    logo_widget.pack(pady=15)

    tk.Label(frame02,
            text = "My Shoes",
            bg = bg01,
            fg="black",
            font=("TkMenuFont", 20)).pack(pady=10)

    for s in shoe_list:
        tk.Label(frame02,text = s, bg = bg02,fg="white",font=("TkHeadingFont", 8)).pack(fill="both")

    tk.Button(frame02,text="Add New Shoe",
                font=("TkHeadingFont", 10),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:Load_Frame03()).pack(pady=5)

    tk.Button(frame02,text="Retire Shoe",
                font=("TkHeadingFont", 10),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:Load_Frame04()).pack(pady=5)

    tk.Button(frame02,text="Add Ks to Shoe",
                font=("TkHeadingFont", 10),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:Load_Frame05()).pack(pady=5)

def Load_Frame03():
    clear_widgets(frame02)
    sort_id()
    frame03.tkraise()
    frame03.pack_propagate(False)

    brand = tk.StringVar()
    model = tk.StringVar()
    color = tk.StringVar()

    logo_image = ImageTk.PhotoImage(file = "ShoeLogo02.png")
    logo_widget = tk.Label(frame03, image=logo_image, bg=bg01)
    logo_widget.image = logo_image
    logo_widget.pack(pady=25)

    tk.Label(frame03,
            text = "Congratulation!! You have new shoe",
            bg = bg01,
            fg="black",
            font=("TkMenuFont", 16)).pack(pady=5)


    tk.Label(frame03,
            text = "shoe brand",
            bg = bg01,
            fg="white",
            font=("TkMenuFont", 14)).pack()


    tk.Entry(frame03, textvariable=brand, width = 20).pack()


    tk.Label(frame03,
            text = "shoe model",
            bg = bg01,
            fg="white",
            font=("TkMenuFont", 14)).pack(pady=1)
    tk.Entry(frame03, textvariable=model, width = 20).pack()

    tk.Label(frame03,
            text = "shoe color",
            bg = bg01,
            fg="white",
            font=("TkMenuFont", 14)).pack(pady=1)
    tk.Entry(frame03, textvariable=color, width = 20).pack()




    tk.Button(frame03,text="Add to DB",
                font=("TkHeadingFont", 10),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:get_entry_frame03(brand,model,color)).pack(pady=5)

    tk.Button(frame03,text="Back",
                font=("TkHeadingFont", 10),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:Load_Frame02()).pack(pady=5)
def Load_Frame04():
    sort_id()
    clear_widgets(frame02)
    clear_widgets(frame04)
    all_sheos = []
    shoe_list = []
    frame04.tkraise()
    frame04.pack_propagate(False)
    id = tk.StringVar()
    all_sheos = fetch_db()
    shoe_list = pre_process(all_sheos)
    logo_image = ImageTk.PhotoImage(file = "ShoeLogo02.png")
    logo_widget = tk.Label(frame04, image=logo_image, bg=bg01)
    logo_widget.image = logo_image
    logo_widget.pack(pady=14)

    tk.Label(frame04,
            text = "You where great! but it is time to go",
            bg = bg01,
            fg="#ccdde3",
            font=("TkMenuFont", 16)).pack(pady=5)


    tk.Label(frame04,
            text = "Enter shoe Id Number to retire",
            bg = bg01,
            fg="white",
            font=("TkMenuFont", 14)).pack()


    tk.Entry(frame04, textvariable=id , width = 20).pack(pady = 10)
    for s in shoe_list:
        tk.Label(frame04,text = s, bg = bg02, fg="white",font=("TkHeadingFont", 8)).pack(fill="both")

    tk.Button(frame04,text="Bye Bye Shoe",
                font=("TkHeadingFont", 10),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:get_entry_frame04(id)).pack(pady=5)

    tk.Button(frame04,text="Back to the List",
                font=("TkHeadingFont", 10),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:Load_Frame02()).pack(pady=5)

def Load_Frame05():
    sort_id()
    clear_widgets(frame05)
    clear_widgets(frame02)
    clear_widgets(frame04)
    frame05.tkraise()
    frame05.pack_propagate(False)
    id = tk.StringVar()
    new_ks = tk.StringVar()
    all_sheos = fetch_db()
    shoe_list = pre_process(all_sheos)
    logo_image = ImageTk.PhotoImage(file = "ShoeLogo02.png")
    logo_widget = tk.Label(frame05, image=logo_image, bg=bg01)
    logo_widget.image = logo_image
    logo_widget.pack(pady=10)

    tk.Label(frame05,
        text = "You run some! Add Ks to DB",
        bg = bg01,
        fg="#ccdde3",
        font=("TkMenuFont", 16)).pack(pady=5)


    for s in shoe_list:
        tk.Label(frame05,text = s,bg = bg02 ,fg="white",font=("TkHeadingFont", 8)).pack(fill="both")
    tk.Label(frame05,
    text = "In which shoe you ran today",
            bg = bg01,fg="white",
            font=("TkMenuFont", 14)).pack()

    tk.Entry(frame05, textvariable=id , width = 20).pack(pady = 7)
    tk.Label(frame05,
            text = "How much?!! Is it a good one?",
            bg = bg01,
            fg="white",
            font=("TkMenuFont", 14)).pack()
    tk.Entry(frame05, textvariable=new_ks , width = 20).pack(pady = 7)

    tk.Button(frame05,text="Add it :)",
                font=("TkHeadingFont", 10),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:get_entry_frame05(id,new_ks)).pack(pady=4)
    tk.Button(frame05,text="Back to the List",
                font=("TkHeadingFont", 10),
                bg=("#182d52"),
                fg=("White"),
                cursor = "hand2",
                activebackground = "#b2c7ed",
                activeforeground = "white",
                command=lambda:Load_Frame02()).pack(pady=4)


def Load_Frame06():
    pass
#load Tkinter
root = tk.Tk()
root.title("Add Shoes")

#root.eval("tk::PlaceWindow . center")
frame01 = tk.Frame(root, width=500, height=500, bg=bg01)
frame02 = tk.Frame(root, width=500, height=600, bg=bg01)
frame03 = tk.Frame(root, bg=bg01)
frame04 = tk.Frame(root, bg=bg01)
frame05 = tk.Frame(root, bg=bg01)
frame06 = tk.Frame(root, bg=bg01)

for frame in (frame01,frame02,frame03, frame04, frame05, frame06):
    frame.grid(row=0, column=0, sticky="nesw")

Load_Frame01()

root.mainloop()
