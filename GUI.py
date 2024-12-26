import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from Def_of_classes import Group, Expenses, Friend
import csv

group_dict={}
group_names="files\\group_names.txt"
group_list=[]

with open(group_names, mode='r') as f :
    reader=f.readlines()
    for row in reader: 
        if row:
            group_list=row.split(",")
            print(row)

#loading group type images
trip=Image.open('pics\\trip.png')
home=Image.open('pics\\home.png')
couple=Image.open('pics\\couple.png')
family=Image.open('pics\\family.png')
party=Image.open('pics\\party.png')
other=Image.open('pics\\other.png')

food=(Image.open('pics\\food.png')).resize((50,50))
shopping=(Image.open('pics\\shopping.png')).resize((50,50))
transportation=(Image.open('pics\\transportation.png')).resize((50,50))
hobby=(Image.open('pics\\hobby.png')).resize((50,50))
medicine=(Image.open('pics\\medicine.png')).resize((50,50))
education=(Image.open('pics\\education.png')).resize((50,50))
gift=(Image.open('pics\\gift.png')).resize((50,50))
business=(Image.open('pics\\business.png')).resize((50,50))
charity=(Image.open('pics\\charity.png')).resize((50,50))



trip=trip.resize((50,50))
home=home.resize((50,50))
couple=couple.resize((50,50))
family=family.resize((50,50))
party=party.resize((50,50))
other=other.resize((50,50))


window=ttk.Window( themename="minty",iconphoto="pics\\icon1.png")
window.geometry('700x650+500+200')
window.title("Splitwise")


Ticon=ImageTk.PhotoImage(trip)
Hicon=ImageTk.PhotoImage(home)
Cicon=ImageTk.PhotoImage(couple)
Ficon=ImageTk.PhotoImage(family)
Picon=ImageTk.PhotoImage(party)
Oicon=ImageTk.PhotoImage(other)

foo_icon=ImageTk.PhotoImage(food)
sh_icon=ImageTk.PhotoImage(shopping)
tr_icon=ImageTk.PhotoImage(transportation)
me_icon=ImageTk.PhotoImage(medicine)
ho_icon=ImageTk.PhotoImage(hobby)
ed_icon=ImageTk.PhotoImage(education)
gi_icon=ImageTk.PhotoImage(gift)
bu_icon=ImageTk.PhotoImage(business)
ch_icon=ImageTk.PhotoImage(charity)


def new_group_page():
    page_1.pack_forget()
    add_group_page.pack()


page_1=ttk.Frame(window, width= 700, height=500)
page_1.pack_propagate(False)
new_button=ttk.Button(master= page_1, text='New Group', command= new_group_page)
new_button.place(x=300,y=20)
page_1.pack()

def return_to_mainpage(current_page):
    current_page.pack_forget()
    page_1.pack()


add_group_page=ttk.Frame(window, width= 700, height=500)
add_group_page.pack_propagate(False)
group_name=tk.StringVar()
group_name_entry=ttk.Entry(add_group_page, textvariable= group_name)
group_name_entry.place(x=320,y=40)
group_name_label=ttk.Label(add_group_page, text="Group name")
group_name_label.place(x=220,y=40)

group_type_label=ttk.Label(add_group_page, text="Group type")
group_type_label.place(x=300,y=120)

selected=tk.StringVar()
radio1=ttk.Radiobutton(master=add_group_page, variable=selected, value='Trip', image=Ticon, text='Trip' ,compound='top')
radio2=ttk.Radiobutton(master=add_group_page, variable=selected, value='Home', image=Hicon, text='Home' ,compound='top')
radio3=ttk.Radiobutton(master=add_group_page, variable=selected, value='Couple', image=Cicon, text='Couple' ,compound='top')
radio4=ttk.Radiobutton(master=add_group_page, variable=selected, value='Family', image=Ficon, text='Family' ,compound='top')
radio5=ttk.Radiobutton(master=add_group_page, variable=selected, value='Party', image=Picon, text='Party' ,compound='top')
radio6=ttk.Radiobutton(master=add_group_page, variable=selected, value='Other', image=Oicon, text='Other' ,compound='top')
radio1.place(x=150,y=170)
radio2.place(x=250,y=170)
radio3.place(x=350,y=170)
radio4.place(x=450,y=170)
radio5.place(x=250,y=270)
radio6.place(x=350,y=270)

def create_group():
    global group_nam
    group_nam=group_name.get().strip()
    if group_nam and selected.get() and group_nam not in group_list:
        group_dict[group_nam]=(Group(group_nam, selected.get()),[])
        group_list.append(group_nam)
        with open(group_names, mode='a') as f :
            f.write(group_nam+',')
        with open(f"files//{group_nam}_{selected.get()}.csv", mode='w') as f :
            pass
        add_group_page.pack_forget()
        group_name_label=ttk.Label(add_friend_page, text=f"Group name:  {group_name.get()}")
        group_name_label.place(x=280,y=30)

        group_type_label=ttk.Label(add_friend_page, text=f"Group type:  {selected.get()}")
        group_type_label.place(x=280,y=70)
        add_friend_page.pack()
        '''add_group_page.entry.delete(0,tk.END)
        add_group_page.radio_var.set("")
        add_group_page.label.place_forget()'''

    elif not group_nam:
        error_label1=ttk.Label(master= add_group_page, text='Please enter a group name.', foreground="red")
        error_label1.place(x=220,y=10)
    elif not selected.get():
        error_label2=ttk.Label(master= add_group_page, text='Please specify a group type.', foreground="red")
        error_label2.place(x=250,y=100)
    else: 
        error_label3=ttk.Label(master= add_group_page, text='The group name already exists, please enter another name.', foreground="red")
        error_label3.place(x=220,y=10)


create_button=ttk.Button(master= add_group_page, text='Create', command= create_group)
create_button.place(x=350,y=380)

main_page_button=ttk.Button(master= add_group_page, text='Main Page', command= lambda: return_to_mainpage(add_group_page))
main_page_button.place(x=335,y=430)

def add_name():
    friend_nam=friend_name.get().strip()
    if friend_nam not in group_dict[group_nam][1]:
        add_friend_name.pack_forget()
        add_friend_page.pack()
        group_dict[group_nam][1].append(friend_nam)
    else:
        error_label=ttk.Label(master= add_friend_name, text='The name already exists, please enter another name.', foreground="red")
        error_label.place(x=100,y=20) 

def add_friend():
    print(group_dict)
    add_friend_page.pack_forget()
    add_friend_name.pack()

def expense_page_func():
    add_friend_page.pack_forget()
    expense_page.pack()
    
add_friend_page=ttk.Frame(window, width= 700, height=500)
add_friend_page.pack_propagate(False)

add_friend_button=ttk.Button(add_friend_page,text='Add person',command=add_friend)
add_friend_button.place(x=300,y=150)

add_expense_button=ttk.Button(master= add_friend_page, text='Add Expenses', command= expense_page_func  )
add_expense_button.place(x=300,y=370)

main_page_button=ttk.Button(master= add_friend_page, text='Main Page', command= lambda: return_to_mainpage(add_friend_page))
main_page_button.place(x=300,y=430)

friend_table=ttk.Treeview(add_friend_page, columns= ('Number','Name'))

add_friend_name=ttk.Frame(master=window ,width= 500, height=400)
add_friend_name.pack_propagate(False)
friend_name=tk.StringVar()
friend_entry=ttk.Entry(master=add_friend_name,textvariable=friend_name)
friend_entry.place(x=220, y=50)
friend_name_label=ttk.Label(master=add_friend_name,text="Please type the name")
friend_name_label.place(x=70, y=50)
add_name_button=ttk.Button(master=add_friend_name,text='Add',command=add_name)
add_name_button.place(x=220, y=110)
main_page_button=ttk.Button(master= add_friend_name, text='Main Page', command= lambda: return_to_mainpage(add_friend_name))
main_page_button.place(x=190,y=350)

friend_table=ttk.Treeview(master= add_friend_page, columns= ('Name','Expense'))
#friend_table.place()

def return_expense_list():
    expense_list_page.pack()
    expense_page.pack_forget()

expense_page=ttk.Frame(master=window ,width= 700, height=700)
expense_page.pack_propagate(False)    

expense_name=tk.StringVar()
expense_name_entry=ttk.Entry(expense_page, textvariable= expense_name)
expense_name_entry.place(x=320,y=30)
expense_name_label=ttk.Label(expense_page, text="Expense name")
expense_name_label.place(x=220,y=30)

expense_payer=tk.StringVar()
expense_payer_entry=ttk.Entry(expense_page, textvariable= expense_name)
expense_payer_entry.place(x=320,y=65)
expense_payer_label=ttk.Label(expense_page, text="Expense Payer")
expense_payer_label.place(x=220,y=65)

expense_owers=tk.StringVar()
expense_owers_entry=ttk.Entry(expense_page, textvariable= expense_owers)
expense_owers_entry.place(x=320,y=100)
expense_owers_label=ttk.Label(expense_page, text="Expense Owers")
expense_owers_label.place(x=215,y=100)

expense_type_label=ttk.Label(expense_page, text="Expense type")
expense_type_label.place(x=300,y=170)

#house, food, shopping, transportation, hobby, medicine, education, gifts, business, pets, charity

selected_extype=tk.StringVar()
radio1=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='food', image=foo_icon, text='Food' ,compound='top')
radio2=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='House', image=Hicon, text='House' ,compound='top')
radio3=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='shopping', image=sh_icon, text='Shopping' ,compound='top')
radio4=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='transportation', image=tr_icon, text='Transport' ,compound='top')
radio5=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='hobby', image=ho_icon, text='Hobby' ,compound='top')
radio6=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='medicine', image=me_icon, text='Medicine' ,compound='top')
radio7=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='education', image=ed_icon, text='Education' ,compound='top')
radio8=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='gift', image=gi_icon, text='Gift' ,compound='top')
radio9=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='business', image=bu_icon, text='Business' ,compound='top')
radio10=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='charity', image=ch_icon, text='Charity' ,compound='top')
radio11=ttk.Radiobutton(master=expense_page, variable=selected_extype, value='Other', image=Oicon, text='Other' ,compound='top')
radio1.place(x=50,y=220)
radio2.place(x=150,y=220)
radio3.place(x=250,y=220)
radio4.place(x=350,y=220)
radio5.place(x=450,y=220)
radio6.place(x=550,y=220)
radio7.place(x=100,y=320)
radio8.place(x=200,y=320)
radio9.place(x=300,y=320)
radio10.place(x=400,y=320)
radio11.place(x=500,y=320)


split_type_label=ttk.Label(expense_page, text="Split type")
split_type_label.place(x=300, y= 430)

split_type=tk.StringVar(value='Equal') #default split is equal
equal=ttk.Radiobutton(master=expense_page, variable=split_type, value='Equal', text='Equal' )
percentage=ttk.Radiobutton(master=expense_page, variable=split_type, value='Percentage', text='Percentage')
portion=ttk.Radiobutton(master=expense_page, variable=split_type, value='Portion', text='Portion')
equal.place(x=180,y=470)
percentage.place(x=280,y=470)
portion.place(x=400,y=470)


main_page_button=ttk.Button(master= expense_page, text='Main Page', command= lambda: return_to_mainpage(expense_page))
main_page_button.place(x=335,y=600)

added_expense_button=ttk.Button(master= expense_page, text='Add', command= return_expense_list)
added_expense_button.place(x=270,y=600)

expense_list_page=ttk.Frame(master=window, width= 700, height=700)
expense_page.pack_propagate(False)

window.mainloop()
