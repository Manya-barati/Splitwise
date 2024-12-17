import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from Def_of_classes import Group, Expenses, Friend

group_list=[]

#loading group type images
trip=Image.open('trip.png')
home=Image.open('home.png')
couple=Image.open('couple.png')
family=Image.open('family.png')
party=Image.open('party.png')
other=Image.open('other.png')

trip=trip.resize((50,50))
home=home.resize((50,50))
couple=couple.resize((50,50))
family=family.resize((50,50))
party=party.resize((50,50))
other=other.resize((50,50))


window=ttk.Window( themename="minty",iconphoto="icon1.png")
window.geometry('700x500+500+200')
window.title("Splitwise")

Ticon=ImageTk.PhotoImage(trip)
Hicon=ImageTk.PhotoImage(home)
Cicon=ImageTk.PhotoImage(couple)
Ficon=ImageTk.PhotoImage(family)
Picon=ImageTk.PhotoImage(party)
Oicon=ImageTk.PhotoImage(other)


def new_group_page():
    page_1.pack_forget()
    add_group_page.pack()


page_1=ttk.Frame(window, width= 700, height=500)
page_1.pack_propagate(False)
new_button=ttk.Button(master= page_1, text='New Group', command= new_group_page)
new_button.place(x=300,y=20)
page_1.pack()

def return_to_mainpage():
    add_group_page.pack_forget()
    page_1.pack()   


add_group_page=ttk.Frame(window, width= 700, height=500)
page_1.pack_propagate(False)
group_name=tk.StringVar()
group_name_entry=ttk.Entry(add_group_page, textvariable= group_name)
group_name_entry.place(x=320,y=30)
group_name_label=ttk.Label(add_group_page, text="Group name")
group_name_label.place(x=220,y=30)

group_type_label=ttk.Label(add_group_page, text="Group type")
group_type_label.place(x=300,y=120)

selected=tk.StringVar()
radio1=ttk.Radiobutton(master=add_group_page, variable=selected, value='trip', image=Ticon, text='Trip' ,compound='top')
radio2=ttk.Radiobutton(master=add_group_page, variable=selected, value='home', image=Hicon, text='Home' ,compound='top')
radio3=ttk.Radiobutton(master=add_group_page, variable=selected, value='couple', image=Cicon, text='Couple' ,compound='top')
radio4=ttk.Radiobutton(master=add_group_page, variable=selected, value='family', image=Ficon, text='Family' ,compound='top')
radio5=ttk.Radiobutton(master=add_group_page, variable=selected, value='party', image=Picon, text='Party' ,compound='top')
radio6=ttk.Radiobutton(master=add_group_page, variable=selected, value='other', image=Oicon, text='Other' ,compound='top')
radio1.place(x=150,y=170)
radio2.place(x=250,y=170)
radio3.place(x=350,y=170)
radio4.place(x=450,y=170)
radio5.place(x=250,y=270)
radio6.place(x=350,y=270)

def create_group():
    group_list.append(Group(group_name,selected))
    add_group_page.pack_forget()
    group_name_label=ttk.Label(add_expense_page, text=f"Group name:  {group_name.get()}")
    group_name_label.place(x=280,y=30)

    group_type_label=ttk.Label(add_expense_page, text=f"Group type:  {selected.get()}")
    group_type_label.place(x=280,y=70)
    add_expense_page.pack()



create_button=ttk.Button(master= add_group_page, text='Create', command= create_group)
create_button.place(x=350,y=380)

main_page_button=ttk.Button(master= add_group_page, text='Main Page', command= return_to_mainpage)
main_page_button.place(x=335,y=430)

def add_friend():
    pass

add_expense_page=ttk.Frame(window, width= 700, height=500)
page_1.pack_propagate(False)

'''group_name_label=ttk.Label(add_expense_page, text=f"Group name: {group_list[0].name}")
group_name_label.place(x=220,y=30)

group_type_label=ttk.Label(add_expense_page, text=f"Group type: {group_list[0].type}")
group_type_label.place(x=220,y=70)'''

add_friend_button=ttk.Button(add_expense_page,text='Add person',command=add_friend)
add_friend_button.place(x=300,y=150)

friend_table=ttk.Treeview(add_expense_page, columns= ('Name','Expense', 'Quota'))
window.mainloop()
