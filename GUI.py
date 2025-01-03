import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from Def_of_classes import Group, Expenses, Friend
import pandas as pd
from detect_cycle import Construct_graph, Delete_Cycle, Greedy_Debt_Simplification, Max_Flow_Simplification
import networkx as nx
import matplotlib.pyplot as plt
from classes_and_results import Group, Friend, Expense, calculate_color, visualize_bar_chart, visualize_pie_chart, visualize_graph
import sqlite3
from functools import partial


conn = sqlite3.connect('login database')  # creating a database
cursor = conn.cursor()     # a curser is used to execute sqlite3 commands

cursor.execute('''CREATE TABLE IF NOT EXISTS friend_names (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            group_name TEXT NOT NULL UNIQUE,
                                                            group_people TEXT DEFAULT "")''')
conn.commit()

"""cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                    username TEXT NOT NULL UNIQUE, 
                                                    password TEXT NOT NULL,
                                                    groups TEXT DEFAULT "")''')      # creating a table for users data
conn.commit()
cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', ('Mahshid', '1382'))
user = cursor.fetchone()
print(user)"""
#cursor.execute('INSERT INTO users(username, password, groups) VALUES (?, ?, ?)', ('John', 'password123', ""))     # inserting the data
"""cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', ('John', 'password123'))
user = cursor.fetchone()   # fetch a single matching row
print(user)
try: 
    cursor.execute('INSERT INTO users(username, password) VALUES (?, ?)', ('John', '987'))
    conn.commit()
except sqlite3.IntegrityError:
    print('username already exists!')

conn.close()"""
#cursor.execute('UPDATE users SET groups = "" WHERE username = ?', ('Mahshid',))

cursor.execute('SELECT * FROM users ')
x=cursor.fetchall()
print(x)

group_dict={}
group_names="files\\group_names.txt"
group_types="files\\group_types.txt"


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

def login_page():
    global login_window, error_label_invalid
    login_window=ttk.Frame(window, width= 700, height=500)
    login_window.pack_propagate(False)

    username_label=ttk.Label(login_window, text='Username:')
    username_label.place(x=230,y=105)
    username=tk.StringVar()
    username_entry = ttk.Entry(master=login_window,textvariable=username)
    username_entry.place(x=310, y=100)

    password_label=ttk.Label(login_window, text='Password:')
    password_label.place(x=230,y=205)
    password=tk.StringVar()
    password_entry = ttk.Entry(master=login_window,textvariable=password, show = '*')
    password_entry.place(x=310, y=200)    

    sign_in_button = ttk.Button(login_window, text= 'sign in', command= lambda: check_sign_in(username, password))
    sign_in_button.place(x= 318, y= 290)

    sign_up_label = ttk.Label(login_window, text = "don't have an account?")
    sign_up_label.place(x= 230, y= 400)
    sign_up_button = ttk.Button(login_window, text= 'create one', command= lambda: sign_up_page())
    sign_up_button.place(x= 360, y= 394)

    error_label_invalid=ttk.Label(login_window, text='', foreground = 'red')
    error_label_invalid.place(x=280, y=335)

    login_window.pack()

def check_sign_in(username, password):
    global current_username

    if not username.get().strip():
        error_label_invalid.config(text = 'Please enter your username')
        return
    if not password.get().strip():
        error_label_invalid.config(text = 'Please enter your password')
        return

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username.get(), password.get()))
    user = cursor.fetchone()
    print(username.get())
    if user:
        current_username = username.get()
        login_window.pack_forget()
        g_table()
        group_table_frame.place(x=50, y=100)
        page_1.pack()
    else:
        error_label_invalid.config(text = 'Invalid username or password')

login_page()

def sign_up_page():
    global signup_window, error_label_signup
    login_window.pack_forget()
    signup_window = ttk.Frame(window, width= 700, height=500)
    signup_window.pack_propagate(False)
    
    name_label=ttk.Label(signup_window, text='Name:')
    name_label.place(x=230,y=85)
    name=tk.StringVar()
    name_entry = ttk.Entry(signup_window, textvariable=name)
    name_entry.place(x=310, y=80)

    username_label=ttk.Label(signup_window, text='Username:')
    username_label.place(x=230,y=185)
    username=tk.StringVar()
    username_entry = ttk.Entry(signup_window, textvariable=username)
    username_entry.place(x=310, y=180)

    password_label=ttk.Label(signup_window, text='Password:')
    password_label.place(x=230,y=285)
    password=tk.StringVar()
    password_entry = ttk.Entry(master=signup_window, textvariable=password, show = '*')
    password_entry.place(x=310, y=280)

    rep_password_label=ttk.Label(signup_window, text='Repeat password:')
    rep_password_label.place(x=200,y=385)
    rep_password=tk.StringVar()
    rep_password_entry = ttk.Entry(master=signup_window, textvariable=rep_password, show = '*')
    rep_password_entry.place(x=310, y=380)

    error_label_signup = ttk.Label(signup_window , text='', foreground = 'red')
    error_label_signup.place(x= 310, y= 480)

    create_button = ttk.Button(signup_window, text= 'Create', command= lambda: check_acount_creation(username, password, name, rep_password))
    create_button.place(x= 340, y=450 )

    signup_window.pack()

def check_acount_creation(username, password, name, rep_password):
    if not username.get().strip() or not password.get().strip() or not name.get().strip() or not rep_password.get().strip():
        error_label_signup.config(text = 'Please fill out all required information.')
        return
    if len(password.get()) < 6:
        error_label_signup.config(text = 'Password should at least be 6 characters')
        return 
    if rep_password.get().strip() != password.get().strip():
        error_label_signup.config(text = 'The repeated password is wrong')
        return

    try:
        cursor.execute('INSERT INTO users(username, password, groups) VALUES (?, ?, ?)', (username.get(), password.get(), ""))
        conn.commit()
        add_previous_groups_for_new_member(username.get())
    except sqlite3.IntegrityError:
        error_label_signup.config(text = 'Username already exists!')
        return
    
    signup_window.pack_forget()
    login_window.pack()

group_list = []
group_tlist = []
def create_group_list():
    cursor.execute('SELECT groups FROM users WHERE username = ?', (current_username, ))
    result = cursor.fetchone()
    if result:
        group_names = result[0]
        if not group_names:
            pass 
        groupp = group_names.split(',')[1:]
        for i in groupp:
            g = i.split('_')
            if g[0] not in group_list:
                group_list.append(g[0])
                group_tlist.append(g[1])

def add_previous_groups_for_new_member(username):
    cursor.execute('SELECT * FROM friend_names') 
    for row in cursor.fetchall():
        people = row[2].split(',')[1:] 
        print(row)
        if username in people:
            cursor.execute('UPDATE users SET groups = groups || ? where username = ?', (f',{row[1]}', username))
            conn.commit()
            

def add_group_for_friends(FriendName, group_name, group_type):
    cursor.execute('SELECT * FROM users')
    for row in cursor.fetchall():
        if row[1] == FriendName:
            cursor.execute('UPDATE users SET groups = groups || ? where username = ?', (f',{group_name}_{group_type}', FriendName))
            conn.commit()

def new_group_page():
    page_1.pack_forget()
    add_group_page.pack()


#to be fixed
def details_page(item_values):
    global file_path, group_name_label, group_type_label
    page_1.pack_forget()

    name=item_values[1]
    type=item_values[2]
    file_path=f"files\\{name}_{type}.csv"

    add_friend_button=ttk.Button(exadd_friend_page,text='Add person',command= lambda: add_friend_prev(exadd_friend_name))
    add_friend_button.place(x=300,y=150)

    add_expense_button=ttk.Button(master= exadd_friend_page, text='Add Expenses', command= lambda: expense_page_func(exadd_friend_page, expense_page2)  )
    add_expense_button.place(x=210,y=530)

    expense_list_button=ttk.Button(master= exadd_friend_page, text='Expenses List', command= expense_list_func  )
    expense_list_button.place(x=350,y=530)

    main_page_button=ttk.Button(master= exadd_friend_page, text='Main Page', command= lambda: return_to_mainpage(exadd_friend_page))
    main_page_button.place(x=300,y=580)
    
    group_name_label.config(text=f"Group name:  {item_values[1]}")  
    group_type_label.config(text=f"Group type:  {item_values[2]}") 
 
    try:
        friend_tabl.pack_forget()
    except:
        pass

    f_tabl(file_path)

    exadd_friend_page.pack()

def switch_back_to_main(current_frame):
    current_frame.pack_forget()
    page_1.pack()

def on_item_select(event):
    global selected_item_details
    selected_item = group_table.focus()
    selected_item_details = group_table.item(selected_item, "values")
    if selected_item_details:
        details_button.config(state=tk.NORMAL)


def add_name_(path,friend_entry, friend_name ):
    global error_label6, error_label7
    friend_nam=friend_name.get().strip()
    with open(path,mode= 'r') as f:
        friends_list= f.readline().split(',')[1:-1]
    #print(friends_list)
    try:
        error_label7.place_forget()
        error_label6.place_forget()
    except:
        pass
    if not friend_nam:
        error_label7=ttk.Label(master= exadd_friend_name, text='Please enter a valid name.', foreground="red")
        error_label7.place(x=100,y=20)       
    elif friend_nam not in friends_list:
        friend_tabl.pack_forget()
        exadd_friend_name.pack_forget()
        friends_list.append(friend_nam)
        print(friend_nam, group_name.get().strip())
        print(selected_item_details)
        cursor.execute('UPDATE friend_names SET group_people = group_people || ? where group_name = ?', (f',{friend_nam}', f'{selected_item_details[1]}_{selected_item_details[2]}'))
        conn.commit()
        add_group_for_friends(friend_nam, selected_item_details[1], selected_item_details[2])
        cursor.execute('SELECT * FROM friend_names')
        group = cursor.fetchall()
        print(group)
        friend_entry.delete(0,tk.END)
        with open(path, mode='r') as f :
            lines= f.readlines()
            with open(path, mode='w') as g:
                if not lines:
                    g.write(','+friend_nam)
                first_line=lines[0].strip()+friend_nam+','
                g.write(first_line)
                for line in lines[1:]:
                    g.write('\n'+line.strip()+'0'+',')
        details_page(selected_item_details)
        try:
          error_label6.place_forget()
        except:
            pass
        #f_tabl(path)  
    else:
        error_label6=ttk.Label(master= exadd_friend_name, text='The name already exists, please enter another name.', foreground="red")
        error_label6.place(x=100,y=20) 


def f_tabl(path):
    global friend_tabl
    with open(path,mode= 'r') as f:
        friends_list= f.readline().split(',')[1:]
    friend_tabl=ttk.Treeview(master= friend_tabl_frame, columns= ('number','name'),show='headings')
    friend_tabl.heading('number', text='Number')
    friend_tabl.heading('name', text='Name')
    for i in range(len(friends_list)-1):
        number=i+1
        name=friends_list[i]
        friend_tabl.insert(parent='', index=tk.END, values=(number,name))
    friend_tabl.pack()


def return_to_mainpage(current_page):
    try:
        error_label1.place_forget()
        error_label2.place_forget()
        error_label3.place_forget()
        error_label4.place_forget()
        error_label5.place_forget()
    except:
        pass
    group_table.pack_forget()
    g_table()
    current_page.pack_forget()
    page_1.pack()

def create_group():
    global group_nam,selected_gtype, error_label1, error_label2, error_label3
    group_nam=group_name.get().strip()
    selected_gtype=selected.get()
    if group_nam and selected_gtype and group_nam not in group_list:
        cursor.execute('UPDATE users SET groups = groups || ? where username = ?', (f',{group_nam}_{selected_gtype}', current_username))
        conn.commit()
        create_group_list()
        print(group_nam)
        cursor.execute('INSERT INTO friend_names (group_name, group_people) VALUES (?, ?)', (f'{group_nam}_{selected_gtype}' ,""))
        conn.commit()
        group_dict[group_nam]=(Group(group_nam, selected_gtype),[])
        with open(f"files//{group_nam}_{selected_gtype}.csv", mode='w') as f :
            pass

        add_group_page.pack_forget()
        group_name_label=ttk.Label(add_friend_page, text=f"Group name:  {group_nam}")
        group_name_label.place(x=280,y=30)

        group_type_label=ttk.Label(add_friend_page, text=f"Group type:  {selected_gtype}")
        group_type_label.place(x=280,y=70)
        add_friend_page.pack()

        add_friend_button=ttk.Button(add_friend_page,text='Add person',command=lambda : add_friend_denovo(add_friend_name))
        add_friend_button.place(x=300,y=150)

        add_expense_button=ttk.Button(master= add_friend_page, text='Add Expenses', command= lambda :expense_page_func(add_friend_page, expense_page1)  )
        add_expense_button.place(x=300,y=550)

        group_name_entry.delete(0,tk.END)
        selected.set("")
        try:
            friend_table.pack_forget()
            error_label1.place_forget()
            error_label2.place_forget()
            error_label3.place_forget()
        except:
            pass
    elif not group_nam:
        error_label1=ttk.Label(master= add_group_page, text='Please enter a group name.', foreground="red")
        try:
            error_label3.place_forget()
        except:
            pass            
        error_label1.place(x=220,y=10)
    elif not selected.get():
        error_label2=ttk.Label(master= add_group_page, text='Please specify a group type.', foreground="red")
        error_label2.place(x=250,y=100)
    else: 
        error_label3=ttk.Label(master= add_group_page, text='The group name already exists, please enter another name.', foreground="red")
        error_label3.place(x=220,y=10)

def add_name(friend_entry, friend_name):
    global error_label4, error_label5
    friend_nam=friend_name.get().strip()
    try:
        error_label5.place_forget()
        error_label4.place_forget()
    except:
        pass
    if not group_dict[group_nam][1]:
        with open(f"files//{group_nam}_{selected_gtype}.csv", mode='a') as f :
            f.write(' ,')
    if not friend_nam:
        error_label5=ttk.Label(master= add_friend_name, text='Please enter a valid name.', foreground="red")
        error_label5.place(x=100,y=20)       
    elif friend_nam not in group_dict[group_nam][1] and friend_nam:
        friend_table.pack_forget()
        add_friend_name.pack_forget()
        add_friend_page.pack()
        group_dict[group_nam][1].append(friend_nam)
        cursor.execute('UPDATE friend_names SET group_people = group_people || ? where group_name = ?', (f',{friend_nam}',f'{group_nam}_{selected_gtype}'))
        conn.commit()            
        add_group_for_friends(friend_nam, group_name.get().strip(), selected_gtype)      
        friend_entry.delete(0,tk.END)
        with open(f"files//{group_nam}_{selected_gtype}.csv", mode='a') as f :
            f.write(friend_nam+',')
        try:
          error_label4.place_forget()
        except:
            pass
        f_table()  
    else:
        error_label4=ttk.Label(master= add_friend_name, text='The name already exists, please enter another name.', foreground="red")
        error_label4.place(x=100,y=20) 

def add_friend_denovo(page_to_pack):
    #print(group_dict)
    friend_name=tk.StringVar()
    friend_entry=ttk.Entry(master=add_friend_name,textvariable=friend_name)
    friend_entry.place(x=220, y=50)
    friend_name_label=ttk.Label(master=add_friend_name,text="Please enter the name")
    friend_name_label.place(x=70, y=50)
    add_name_button=ttk.Button(master=add_friend_name,text='Add',command= lambda: add_name(friend_entry, friend_name))
    add_name_button.place(x=220, y=200)

    add_friend_page.pack_forget()
    add_friend_name.pack()

def add_friend_prev(page_to_pack):
    #print(group_dict)

    friend_name=tk.StringVar()
    friend_entry=ttk.Entry(master=exadd_friend_name,textvariable=friend_name)
    friend_entry.place(x=220, y=50)
    friend_name_label=ttk.Label(master=exadd_friend_name,text="Please enter the name")
    friend_name_label.place(x=70, y=50)
    add_name_button=ttk.Button(master=exadd_friend_name,text='Add',command= lambda: add_name_(file_path, friend_entry,friend_name))
    add_name_button.place(x=220, y=200)

    exadd_friend_page.pack_forget()
    exadd_friend_name.pack()

def expense_page_func(page_to_forget, page_to_pack):
    expense_stuffs(page_to_pack)
    page_to_forget.pack_forget()
    page_to_pack.pack()

def f_table():
    global friend_table
    friend_table=ttk.Treeview(master= friend_table_frame, columns= ('number','name'),show='headings')
    friend_table.heading('number', text='Number')
    friend_table.heading('name', text='Name')
    for i in range(len(group_dict[group_nam][1])):
        number=i+1
        name=group_dict[group_nam][1][i]
        friend_table.insert(parent='', index=tk.END, values=(number,name))
    friend_table.pack()

def return_expense_list(expense_page,expense_name, expense_amount, expense_payer, expense_owers, selected_extype, split_type, expense_share):
    if expense_page== expense_page1:
        path=f"files//{group_nam}_{selected_gtype}.csv"
    else:
        path= file_path
    expense_list=[]
    amount_list=[]
    extype_list=[]
    payer_list=[]
    df= pd.read_csv(path)
    try:    
        df = df.iloc[:, :-1]
        df = df.set_index(df.columns[0])
    except:
        pass
    friends_list=list(df.columns)
    for i in list(df.index):
        e= i.split('_')
        expense_list.append(e[0])
        amount_list.append(e[1])
        extype_list.append(e[2])
        payer_list.append(e[3])
    
    expense_nam= expense_name.get().strip()
    expense_amoun=expense_amount.get()
    try:
        expense_amoun=float(expense_amoun)
    except:
        error_label8=ttk.Label(master= expense_page, text='Please enter a valid expense amount.', foreground="red")
        error_label8.place(x=250,y=100)
    expense_paye= expense_payer.get().strip()
    expense_ower= expense_owers.get().split(',')
    expense_ower=[x.strip() for x in expense_ower]
    extyp= selected_extype.get()
    split_typ= split_type.get() 
    share= expense_share.get().split(',')
    if split_typ!='Equal':
        try:
            share=[float(x.strip()) for x in share]
        except:
            error_label9=ttk.Label(master= expense_page, text='Please enter a valid expense share.', foreground="red")
            error_label9.place(x=250,y=100) 

    people=[expense_paye]+expense_ower
    if not expense_nam or not expense_amoun or not expense_paye or not expense_ower or not extyp:
        error_label5=ttk.Label(master= add_group_page, text='Please fill the entries or select an expense type .', foreground="red")
        error_label5.place(x=250,y=100)
    elif expense_nam not in expense_list and expense_paye in friends_list and all(ower in friends_list for ower in expense_ower) :
        if expense_page== expense_page1:
            try:
                expense_table.pack_forget()
            except:
                pass
        try:
            expense_tabl.pack_forget()
        except:
            pass
        expense_list.append(expense_nam)
        amount_list.append(expense_amoun)
        extype_list.append(extyp)
        payer_list.append(expense_paye)
        if split_typ=='Equal':
            share=[1/len(people) for x in people]
            exp_dict={friend:shar for (friend,shar) in zip(people,share)}
        elif split_typ=='Percentage':
            share=[x/100 for x in share]
            exp_dict={friend:shar for (friend,shar) in zip(people,share)}
        else:
            sum_=sum(share)
            share=[x/sum_ for x in share]
            exp_dict={friend:shar for (friend,shar) in zip(people,share)}
        whole_share=[]
        for fr in friends_list:
            if fr in exp_dict:
                whole_share.append(exp_dict[fr])
            else:
                whole_share.append(0)
        whole_share=[str(x) for x in whole_share]
        with open(path, mode='a') as f :
            f.write("\n"+f'{expense_nam}_{expense_amoun}_{extyp}_{expense_paye}'+",")
            f.write(",".join(whole_share)+",")
        if expense_page== expense_page1:
            ex_table(path)
            expense_list_page.pack()
        else:
            ex_tabl(file_path)
            exexpense_list_page.pack()            
        expense_page.pack_forget()
        

def expense_list_func():
    try:
        expense_tabl.pack_forget()
    except:
        pass
    ex_tabl(file_path)
    exadd_friend_page.pack_forget()
    exexpense_list_page.pack()


def change_state(expense_share_entry):
    expense_share_entry.config(state=tk.NORMAL)
def off_state(expense_share_entry):
    expense_share_entry.config(state=tk.DISABLED)

def ex_table(path):
    global expense_table
    expense_table=ttk.Treeview(master= expense_table_frame, columns= ('number','ex_name','ex_type','ex_amount','payer'),show='headings')
    expense_table.heading('number', text='Number')
    expense_table.heading('ex_name', text='Expense Name')
    expense_table.heading('ex_type', text='Expense Type')
    expense_table.heading('ex_amount', text='Expense Amount')
    expense_table.heading('payer', text='Payer')
    expense_table.column('ex_name', width=130)
    expense_table.column('ex_type', width=130)
    expense_table.column('ex_amount', width=130)
    expense_table.column('payer', width=130)
    expense_table.column('number', width=100)
    df= pd.read_csv(path)
    df = df.iloc[:, :-1]
    df = df.set_index(df.columns[0])
    for i in range(len(list(df.index))):
        number=i+1
        elements=list(df.index)[i].split('_')
        #print(elements)
        name= elements[0]
        ex_type= elements[2]
        amount= elements[1]
        payer= elements[3]
        expense_table.insert(parent='', index=tk.END, values=(number, name, ex_type, amount, payer))
    expense_table.pack()


def ex_tabl(path):
    global expense_tabl
    expense_tabl=ttk.Treeview(master= expense_tabl_frame, columns= ('number','ex_name','ex_type','ex_amount','payer'),show='headings')
    expense_tabl.heading('number', text='Number')
    expense_tabl.heading('ex_name', text='Expense Name')
    expense_tabl.heading('ex_type', text='Expense Type')
    expense_tabl.heading('ex_amount', text='Expense Amount')
    expense_tabl.heading('payer', text='Payer')
    expense_tabl.column('ex_name', width=130)
    expense_tabl.column('ex_type', width=130)
    expense_tabl.column('ex_amount', width=130)
    expense_tabl.column('payer', width=130)
    expense_tabl.column('number', width=100)
    df= pd.read_csv(path)
    df = df.iloc[:, :-1]
    df = df.set_index(df.columns[0])
    for i in range(len(list(df.index))):
        number=i+1
        elements=list(df.index)[i].split('_')
        #print(elements)
        name= elements[0]
        ex_type= elements[2]
        amount= elements[1]
        payer= elements[3]
        expense_tabl.insert(parent='', index=tk.END, values=(number, name, ex_type, amount, payer))
    expense_tabl.pack(fill=tk.BOTH, expand=True)        

def search_items(path):
    
    if path== file_path:
        query = exsearch_var.get().lower()
        exp_table=expense_tabl
    else:
        query = search_var.get().lower()
        exp_table=expense_table
    df= pd.read_csv(path)
    df = df.iloc[:, :-1]
    df = df.set_index(df.columns[0])

    idx_list=[]
    for index in df.index:
        if query in str(index).lower():
            ex_name=index.split("_")[0]
            idx_list.append(ex_name)
            pass #highlighting
    for coldex in df.columns:
        if query in str(coldex).lower():
            for index in df.index:
                if df.loc[index,coldex]!=0:
                    ex_name=index.split("_")[0]
                    if ex_name not in idx_list:
                        idx_list.append(ex_name)
                    pass #highlighting rows
   
    for child in exp_table.get_children():
        exp_table.item(child, tags="")
        for match in idx_list:
            value=exp_table.item(child, 'values')
            if match in value:
                exp_table.item(child, tags=("highlight",))

    exp_table.tag_configure("highlight", background="lightblue")

def reset_search(path):
    if path== file_path:
        exsearch_var.set("")
        exp_table=expense_tabl
    else:
        search_var.set("")
        exp_table=expense_table
    search_var.set("")
    exsearch_var.set("")
      # Clear the search bar
    for child in exp_table.get_children():
        exp_table.item(child, tags="")  # Clear all tags
    exp_table.tag_configure("highlight", background="white")  # Reset background



selected_item_details = None

page_1=ttk.Frame(window, width= 700, height=500)
page_1.pack_propagate(False)

details_button = ttk.Button(master=page_1, text="Details", state=tk.DISABLED, command= lambda : details_page(selected_item_details))
details_button.place(x=300, y=350)

new_button=ttk.Button(master= page_1, text='New Group', command= new_group_page)
new_button.place(x=300,y=20)

group_table_frame=ttk.Frame(master=page_1,width= 100, height=100)

def g_table():
    global group_table
    group_table=ttk.Treeview(master= group_table_frame, columns= ('number','g_name','g_type'),show='headings')
    group_table.heading('number', text='Number')
    group_table.heading('g_name', text='Group Name')
    group_table.heading('g_type', text='Group Type')
    create_group_list()
    print(group_list)
    for i in range(len(group_list)):
        number=i+1
        name=group_list[i]
        g_type=group_tlist[i]
        group_table.insert(parent='', index=tk.END, values=(number,name,g_type))
    group_table.bind("<<TreeviewSelect>>", on_item_select)
    group_table.pack()
#g_table()
#group_table_frame.place(x=50, y=100)
#page_1.pack()

def calculate_trans(page_to_forget,path):
    df= pd.read_csv(path)
    df = df.iloc[:, :-1]
    df = df.set_index(df.columns[0])

    transaction_list = []
    
    for idx, row in df.iterrows():
        split_idx = idx.split('_')
        payer = split_idx[-1]
        expense_amount = float(split_idx[1])
        
        for col, value in row.items():
            if value != 0 and col != payer:
                # Calculate the amount
                amount = value * expense_amount
                # Append the transaction details to the list
                transaction_list.append([col, payer, amount])
    Graph= Construct_graph(transaction_list)
    Graph.construct_transaction_dict()
    #print(Graph.trans_dict)
    graph_1 = Graph.convert_to_dict_graph()
    #print('initial graph', graph_1, '\n')

    Cycle = Delete_Cycle(graph_1)
    graph_2 = Cycle.answer()

    greedy= Greedy_Debt_Simplification(graph_2)
    graph_4 = greedy.answer()

    list_tr=convert_dict_to_list(graph_4)
    create_transaction_ui(result_page,list_tr)

    show_graph_button=ttk.Button(master= result_page, text='Show Graph', command= lambda: return_to_mainpage(result_page))
    show_graph_button.place(x=200,y=450)

    balances_button=ttk.Button(master= result_page, text='Balances', command= lambda: return_to_mainpage(result_page))
    balances_button.place(x=400,y=450)

    exp_chart_button=ttk.Button(master= result_page, text='Main Page', command= lambda: return_to_mainpage(result_page))
    exp_chart_button.place(x=200,y=550)

    unpaid_chart_button=ttk.Button(master= result_page, text='Main Page', command= lambda: return_to_mainpage(result_page))
    unpaid_chart_button.place(x=400,y=550)


    page_to_forget.pack_forget()
    result_page.pack()

def convert_dict_to_list(in_dict):
    tr_list=[]
    for key,value in in_dict.items():
        if value:
            for ikey,ivalue in value.items():
                tr_list.append([key,ikey,ivalue])
    return tr_list

def create_transaction_ui(root, transactions):
    canvas = ttk.Canvas(root, width=400, height=300, bg="white")
    canvas.place(x=75, y=10)

    y_offset = 50  # Initial y-coordinate for arrows
    row=1
    for transaction in transactions:
        person1, person2, value = transaction
        
        # Draw arrow and label
        x1, y1 = 100, y_offset
        x2, y2 = 300, y_offset
        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
        canvas.create_text((x1 + x2) / 2, y1 - 10, text="{:0.2f}".format(value), fill="blue")
        canvas.create_text(x1 - 50, y1, text=person1, anchor="e", fill="black")
        canvas.create_text(x2 + 50, y2, text=person2, anchor="w", fill="black")
        
        # creates extra buttons!!!
        btn = ttk.Button(root, text="Unpaid", state = 'disabled')
        btn.place(x=x2 + 250, y=y_offset - 5) 
        if person2 == current_username:
            btn['state'] = 'normal'
            btn.config(command = lambda b= btn: settle_payment(b))
        y_offset += 50
        row+=1



def settle_payment(btn):
    btn.config(text = 'Settled', state = 'disabled')

add_group_page=ttk.Frame(window, width= 700, height=500)
add_group_page.pack_propagate(False)
group_name=tk.StringVar()
group_name_entry=ttk.Entry(add_group_page, textvariable= group_name)
group_name_entry.place(x=320,y=40)
group_name_label=ttk.Label(add_group_page, text="Group name")
group_name_label.place(x=220,y=40)

group_type_label=ttk.Label(add_group_page, text="Group type")
group_type_label.place(x=300,y=120)

selected=tk.StringVar(value="")
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


create_button=ttk.Button(master= add_group_page, text='Create', command= create_group)
create_button.place(x=350,y=380)

main_page_button=ttk.Button(master= add_group_page, text='Main Page', command= lambda: return_to_mainpage(add_group_page))
main_page_button.place(x=335,y=430)
   
add_friend_page=ttk.Frame(window, width= 700, height=700)
add_friend_page.pack_propagate(False)

main_page_button=ttk.Button(master= add_friend_page, text='Main Page', command= lambda: return_to_mainpage(add_friend_page))
main_page_button.place(x=300,y=600)

exadd_friend_page=ttk.Frame(window, width= 700, height=700)
exadd_friend_page.pack_propagate(False)

group_name_label=ttk.Label(exadd_friend_page, text="")
group_name_label.place(x=280,y=30)

group_type_label=ttk.Label(exadd_friend_page , text="")
group_type_label.place(x=280,y=70) 

friend_table=ttk.Treeview(add_friend_page, columns= ('Number','Name'))

add_friend_name=ttk.Frame(master=window ,width= 500, height=400)
add_friend_name.pack_propagate(False)


main_page_button=ttk.Button(master= add_friend_name, text='Main Page', command= lambda: return_to_mainpage(add_friend_name))
main_page_button.place(x=190,y=300)

exadd_friend_name=ttk.Frame(master=window ,width= 500, height=400)
exadd_friend_name.pack_propagate(False)


main_page_button=ttk.Button(master= exadd_friend_name, text='Main Page', command= lambda: return_to_mainpage(exadd_friend_name))
main_page_button.place(x=190,y=300)

friend_table_frame=ttk.Frame(add_friend_page,width= 50, height=50)
friend_table_frame.place(x=150, y=250)

friend_tabl_frame=ttk.Frame(master= exadd_friend_page ,width= 50, height=50)
friend_tabl_frame.place(x=150, y=250)

expense_page1=ttk.Frame(master=window ,width= 700, height=700)
expense_page1.pack_propagate(False)   

expense_page2=ttk.Frame(master=window ,width= 700, height=700)
expense_page2.pack_propagate(False)

def expense_stuffs(expense_page):
    expense_name=tk.StringVar()
    expense_name_entry=ttk.Entry(expense_page, textvariable= expense_name)
    expense_name_entry.place(x=320,y=30)
    expense_name_label=ttk.Label(expense_page, text="Expense name")
    expense_name_label.place(x=220,y=30)

    expense_amount=tk.StringVar()
    expense_amount_entry=ttk.Entry(expense_page, textvariable= expense_amount)
    expense_amount_entry.place(x=320,y=65)
    expense_amount_label=ttk.Label(expense_page, text="Expense amount")
    expense_amount_label.place(x=205,y=65)

    expense_payer=tk.StringVar()
    expense_payer_entry=ttk.Entry(expense_page, textvariable= expense_payer)
    expense_payer_entry.place(x=320,y=100)
    expense_payer_label=ttk.Label(expense_page, text="Expense Payer")
    expense_payer_label.place(x=220,y=100)

    expense_owers=tk.StringVar()
    expense_owers_entry=ttk.Entry(expense_page, textvariable= expense_owers)
    expense_owers_entry.place(x=320,y=135)
    expense_owers_label=ttk.Label(expense_page, text="Expense Owers")
    expense_owers_label.place(x=215,y=135)

    expense_type_label=ttk.Label(expense_page, text="Expense type")
    expense_type_label.place(x=300,y=190)

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
    equal=ttk.Radiobutton(master=expense_page, variable=split_type, value='Equal', text='Equal', command=  lambda: off_state(expense_share_entry) )
    percentage=ttk.Radiobutton(master=expense_page, variable=split_type, value='Percentage', text='Percentage',command= lambda: change_state(expense_share_entry) )
    portion=ttk.Radiobutton(master=expense_page, variable=split_type, value='Portion', text='Portion',command= lambda: change_state(expense_share_entry) )
    equal.place(x=180,y=470)
    percentage.place(x=280,y=470)
    portion.place(x=400,y=470)

    expense_share=tk.StringVar()
    expense_share_entry=ttk.Entry(expense_page, state= tk.DISABLED ,textvariable= expense_share)
    expense_share_entry.place(x=290,y=520)
    expense_share_label=ttk.Label(expense_page, text="Share list")
    expense_share_label.place(x=215,y=520)

    main_page_button=ttk.Button(master= expense_page, text='Main Page', command= lambda: return_to_mainpage(expense_page))
    main_page_button.place(x=335,y=600)

    added_expense_button=ttk.Button(master= expense_page, text='Add', command= lambda : return_expense_list(expense_page,expense_name, expense_amount, expense_payer, expense_owers, selected_extype, split_type, expense_share))
    added_expense_button.place(x=270,y=600)

expense_list_page=ttk.Frame(master=window, width= 700, height=700)
expense_list_page.pack_propagate(False)

expense_table_frame=ttk.Frame(master=expense_list_page,width=300, height=400)
expense_table_frame.place(x=50, y=100)

main_page_button=ttk.Button(master= expense_list_page, text='Main Page', command= lambda: return_to_mainpage(expense_list_page))
main_page_button.place(x=335,y=600)

add_expense_button=ttk.Button(master= expense_list_page, text='Add Expenses', command= lambda: expense_page_func(expense_list_page,expense_page1)  )
add_expense_button.place(x=300,y=550)

calculate_button=ttk.Button(master= expense_list_page, text='Caluclate Transactions', command= lambda: calculate_trans(expense_list_page, f"files//{group_nam}_{selected_gtype}.csv" ) )
calculate_button.place(x=300,y=500)

search_var = tk.StringVar()
search_bar = ttk.Entry(expense_list_page, textvariable=search_var, width=30)
search_bar.place(x=300, y=10)

search_button = ttk.Button(expense_list_page, text="Search", command=lambda : search_items(f"files//{group_nam}_{selected_gtype}.csv"))
search_button.place(x=300, y=10)

reset_button = ttk.Button(expense_list_page, text="Reset", command= lambda : reset_search(f"files//{group_nam}_{selected_gtype}.csv"))
reset_button.place(x=350, y=10)

#existing group expenses
exexpense_list_page=ttk.Frame(master=window, width= 700, height=700)
exexpense_list_page.pack_propagate(False)

expense_tabl_frame=ttk.Frame(master=exexpense_list_page,width=200, height=400)
expense_tabl_frame.place(x=50, y=100)

main_page_button=ttk.Button(master= exexpense_list_page, text='Main Page', command= lambda: return_to_mainpage(exexpense_list_page))
main_page_button.place(x=335,y=550)

add_expense_button=ttk.Button(master= exexpense_list_page, text='Add Expenses', command= lambda: expense_page_func(exexpense_list_page,expense_page2)  )
add_expense_button.place(x=330,y=500)

excalculate_button=ttk.Button(master= exexpense_list_page, text='Caluclate Transactions', command= lambda: calculate_trans(exexpense_list_page, file_path)  )
excalculate_button.place(x=300,y=450)

exsearch_var = tk.StringVar()
search_bar = ttk.Entry(exexpense_list_page, textvariable=exsearch_var, width=20)
search_bar.place(x=280, y=10)

search_button = ttk.Button(exexpense_list_page, text="Search", command= lambda : search_items(file_path))
search_button.place(x=400, y=10)

reset_button = ttk.Button(exexpense_list_page, text="Reset", command= lambda : reset_search(file_path))
reset_button.place(x=480, y=10)

result_page=ttk.Frame(window, width= 700, height=700)
result_page.pack_propagate(False)

main_page_button=ttk.Button(master= result_page, text='Main Page', command= lambda: return_to_mainpage(result_page))
main_page_button.place(x=300,y=600)



window.mainloop()
