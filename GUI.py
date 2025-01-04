import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from Def_of_classes import Group, Expenses, Friend
import pandas as pd
from detect_cycle import Construct_graph, Delete_Cycle, Greedy_Debt_Simplification, Max_Flow_Simplification, final_answer
import networkx as nx
import matplotlib.pyplot as plt
from classes_and_results import Group, Friend, Expense, calculate_color, visualize_bar_chart, visualize_pie_chart, visualize_graph, generate_colors
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date
import re


todate=str(date.today()).split('-')
today=todate[1]+'/'+todate[2]+'/'+todate[0]

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
#this prevents unwanted errors
file_path=''

#this dictionary saves new groups data
group_dict={}

#these two lists will save group names and group types
group_list = []
group_tlist = []

#loading group type images
trip=Image.open('pics\\trip.png').resize((50,50))
home=Image.open('pics\\home.png').resize((50,50))
couple=Image.open('pics\\couple.png').resize((50,50))
family=Image.open('pics\\family.png').resize((50,50))
party=Image.open('pics\\party.png').resize((50,50))
other=Image.open('pics\\other.png').resize((50,50))
#loading expense type images
food=(Image.open('pics\\food.png')).resize((50,50))
shopping=(Image.open('pics\\shopping.png')).resize((50,50))
transportation=(Image.open('pics\\transportation.png')).resize((50,50))
hobby=(Image.open('pics\\hobby.png')).resize((50,50))
medicine=(Image.open('pics\\medicine.png')).resize((50,50))
education=(Image.open('pics\\education.png')).resize((50,50))
gift=(Image.open('pics\\gift.png')).resize((50,50))
business=(Image.open('pics\\business.png')).resize((50,50))
charity=(Image.open('pics\\charity.png')).resize((50,50))


window=ttk.Window( themename="minty",iconphoto="pics\\icon1.png")
window.geometry('950x700+500+200')
window.title("Splitwise")

#load the image in Tkinter
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


# command of "new_button" which shows the creating group page
def new_group_page():
    page_1.pack_forget()
    add_group_page.pack()

# command of "details_button" which shows the details of an existing group
def details_page(item_values):
    global file_path, group_name_label, group_type_label
    page_1.pack_forget()

    name=item_values[1]
    type=item_values[2]
    file_path=f"files\\{name}_{type}.csv"

    add_friend_button=ttk.Button(exadd_friend_page,text='Add person',command= add_friend_prev)
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

# binding function of group table which turn details button enable when a row in the table is selected
def on_item_select(event):
    global selected_item_details
    selected_item = group_table.focus()
    selected_item_details = group_table.item(selected_item, "values")
    if selected_item_details:
        details_button.config(state=tk.NORMAL)

# command of main page buttons, show main page and updates group table
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

# command of "create_button" ,checks some conditions for creating a new group
def create_group():
    global group_nam,selected_gtype, error_label1, error_label2, error_label3
    group_nam=group_name.get().strip()
    selected_gtype=selected.get()
    path=f"files//{group_nam}_{selected_gtype}.csv"
    if group_nam and selected_gtype and group_nam not in group_list:
        cursor.execute('UPDATE users SET groups = groups || ? where username = ?', (f',{group_nam}_{selected_gtype}', current_username))
        conn.commit()
        create_group_list()
        print(group_nam)
        cursor.execute('INSERT INTO friend_names (group_name, group_people) VALUES (?, ?)', (f'{group_nam}_{selected_gtype}' ,""))
        conn.commit()
        group_dict[group_nam]=(Group(group_nam, selected_gtype),[])
        with open(f"files//{group_nam}_{selected_gtype}.csv", mode='w') as f :
            f.write(' ,'+current_username+',')
        group_dict[group_nam][1].append(current_username)
        add_group_page.pack_forget()
        group_name_label=ttk.Label(add_friend_page, text=f"Group name:  {group_nam}")
        group_name_label.place(x=280,y=30)

        group_type_label=ttk.Label(add_friend_page, text=f"Group type:  {selected_gtype}")
        group_type_label.place(x=280,y=70)
    
        add_friend_page.pack()

        add_friend_button=ttk.Button(add_friend_page,text='Add person',command= add_friend_denovo)
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
    friends_list=group_dict[group_nam][1]
    friend_nam=friend_name.get().split(',')
    friend_nam=[friend.strip() for friend in friend_nam]
    for i in friend_nam:
        if i=='':
            friend_nam=False
            break
    try:
        error_label5.place_forget()
        error_label4.place_forget()
    except:
        pass
    if not group_dict[group_nam][1]:
        with open(f"files//{group_nam}_{selected_gtype}.csv", mode='a') as f :
            f.write(' ,')
    if not friend_nam:
        error_label5=ttk.Label(master= add_friend_name, text='Please enter a valid name or a valid list of names.', foreground="red")
        error_label5.place(x=100,y=20)       
    elif not any(friend in friends_list for friend in friend_nam ):
        friend_table.pack_forget()
        add_friend_name.pack_forget()
        add_friend_page.pack()
        group_dict[group_nam][1].append(friend_nam)     
        friend_entry.delete(0,tk.END)
        for fr in friend_nam:
            group_dict[group_nam][1].append(fr)
            with open(f"files//{group_nam}_{selected_gtype}.csv", mode='a') as f :
                f.write(fr+',')
            cursor.execute('UPDATE friend_names SET group_people = group_people || ? where group_name = ?', (f',{friend_nam}',f'{group_nam}_{selected_gtype}'))
            conn.commit()            
            add_group_for_friends(friend_nam, group_name.get().strip(), selected_gtype) 
        try:
          error_label4.place_forget()
        except:
            pass
        f_table()  
    else:
        error_label4=ttk.Label(master= add_friend_name, text='The name already exists, please enter another name.', foreground="red")
        error_label4.place(x=100,y=20) 
def add_name_(path,friend_entry, friend_name ):
    global error_label6, error_label7
    friend_nam=friend_name.get().split(',')
    friend_nam=[friend.strip() for friend in friend_nam]
    with open(path,mode= 'r') as f:
        friends_list= f.readline().split(',')[1:-1]
    #print(friends_list)
    try:
        error_label7.place_forget()
        error_label6.place_forget()
    except:
        pass
    for i in friend_nam:
        if i=='':
            friend_nam=False
            break

    if not friend_nam:
        error_label7=ttk.Label(master= exadd_friend_name, text='Please enter a valid name or a valid list of names.', foreground="red")
        error_label7.place(x=100,y=20)       
    elif not any(friend in friends_list for friend in friend_nam ) :
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
        for fr in friend_nam:
            with open(path, mode='r') as f :
                lines= f.readlines()
                with open(path, mode='w') as g:
                    if not lines:
                        g.write(','+fr)
                    first_line=lines[0].strip()+fr+','
                    g.write(first_line)
                    for line in lines[1:]:
                        g.write('\n'+line.strip()+'0'+',')
        details_page(selected_item_details)
        try:
          error_label6.place_forget()
        except:
            pass 
    else:
        error_label6=ttk.Label(master= exadd_friend_name, text='The name or one of the names already exists, please enter another name.', foreground="red")
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

#command of "add_friend_button" for new groups
def add_friend_denovo():

    friend_name=tk.StringVar()
    friend_entry=ttk.Entry(master=add_friend_name,textvariable=friend_name)
    friend_entry.place(x=220, y=50)
    friend_name_label=ttk.Label(master=add_friend_name,text="Please enter the name")
    friend_name_label.place(x=70, y=50)
    friend_name_labe=ttk.Label(master=add_friend_name,text="You can also enter a list of comma seperated names,\n be aware that the names must be unique",foreground='gray')
    friend_name_labe.place(x=50, y=100)
    add_name_button=ttk.Button(master=add_friend_name,text='Add',command= lambda: add_name(friend_entry, friend_name))
    add_name_button.place(x=220, y=200)

    add_friend_page.pack_forget()
    add_friend_name.pack()

#command of "add_friend_button" for existing groups
def add_friend_prev():
    #command,forgetting page and packing page are different
    friend_name=tk.StringVar()
    friend_entry=ttk.Entry(master=exadd_friend_name,textvariable=friend_name)
    friend_entry.place(x=220, y=50)
    friend_name_label=ttk.Label(master=exadd_friend_name,text="Please enter the name")
    friend_name_label.place(x=70, y=50)
    friend_name_labe=ttk.Label(master=exadd_friend_name,text="You can also enter a list of comma seperated names,\n be aware that the names must be unique")
    friend_name_labe.place(x=50, y=100)
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


def return_expense_list(expense_page,expense_name, expense_amount, expense_payer, expense_owers, selected_extype, split_type, expense_share, recurrency_type,expense_date,expense_curr):

    if expense_page== expense_page1:
        path=f"files//{group_nam}_{selected_gtype}.csv"
        error_label=error_label8
    else:
        path= file_path
        error_label=error_label9
    error_label.place(x=120,y=7)
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
        expense_amoun=False
    expense_paye= expense_payer.get().strip()
    expense_ower= expense_owers.get().split(',')
    expense_ower=[x.strip() for x in expense_ower]
    print(expense_ower)
    extyp= selected_extype.get()
    split_typ= split_type.get() 
    share= expense_share.get().split(',')
    recur_type=recurrency_type.get()
    expense_dat= expense_date.get()
    date_pattern = r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/(19|20)\d\d$'
    if re.match(date_pattern,expense_dat):
        expense_date_=expense_dat.split('/')
        expense_dat=expense_date_[2]+'-'+expense_date_[0]+'-'+expense_date_[1]
    else:
        expense_dat=False
    print(expense_dat)
    expense_cur=expense_curr.get()
    people=[expense_paye]+expense_ower
    if split_typ!='Equal':
        try:
            share=[float(x.strip()) for x in share]
            if split_typ=='Percentage':
                if sum(share)!=100:
                    share=False
        except:
            share=False
    else:
        share=[1/len(people) for i in people]

    if not expense_nam or not expense_paye or expense_ower==[''] :
        error_label.config(text='Please fill the entries .')
    elif not expense_amoun:
        error_label.config(text= "Please enter a valid expense amount.")
    elif not extyp:
        error_label.config(text='Please select an expense type .')
    elif expense_nam in expense_list:
        error_label.config(text='The expense name already exists, please enter another name.')
    elif expense_paye not in friends_list :
        error_label.config(text='There is not such person in the list of members, please enter another payer.')
    elif not all(ower in friends_list for ower in expense_ower):
        error_label.config(text='There is not such person or people in the list of members, please revise the list of owers.')
    elif not share or len(share)!=len(people):
        error_label.config(text='Please enter a valid list of expense shares.')
    elif not expense_dat:
        error_label.config(text='Please enter a valid date according to the desired pattern.')
    elif expense_nam not in expense_list and expense_paye in friends_list and all(ower in friends_list for ower in expense_ower) :
        if expense_page== expense_page1:
            try:
                expense_table.pack_forget()
            except:
                pass
        else:
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
            f.write("\n"+f'{expense_nam}_{expense_amoun}_{extyp}_{expense_paye}_{recur_type}_{expense_dat}_{expense_cur}'+",")
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
    expense_table.bind("<<TreeviewSelect>>", on_exitem_select)
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
    expense_tabl.bind("<<TreeviewSelect>>", exon_exitem_select)
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
    friends_list=list(df.columns)
    transaction_list = []
    
    for idx, row in df.iterrows():
        split_idx = idx.split('_')
        payer = split_idx[3]
        expense_amount = float(split_idx[1])
        
        for col, value in row.items():
            if value != 0 and col != payer:
                # Calculate the amount
                amount = value * expense_amount
                # Append the transaction details to the list
                transaction_list.append([col, payer, amount])
    Graph= Construct_graph(transaction_list)
    Graph.construct_transaction_dict()

    graph_1 = Graph.convert_to_dict_graph()

    graph_2,centr = final_answer(transaction_list)

    list_tr=convert_dict_to_list(graph_2)
    create_transaction_ui(result_page,list_tr)

    show_graph_button=ttk.Button(master= result_page, text='Show Graph', command= lambda: show_graph(graph_1, graph_2 ))
    show_graph_button.place(x=50,y=500,width=150, height=50)

    balances_button=ttk.Button(master= result_page, text='Balances', command= lambda: balances(graph_2,friends_list))
    balances_button.place(x=220,y=500 ,width=100, height=50)

    exp_chart_button=ttk.Button(master= result_page, text='Expense Chart', command= lambda: expense_chart(df))
    exp_chart_button.place(x=340,y=500,width=150, height=50)

    unpaid_chart_button=ttk.Button(master= result_page, text='Unpaid Chart', command= lambda: return_to_mainpage(result_page))
    unpaid_chart_button.place(x=510,y=500,width=150, height=50)


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

def show_graph(prev_graph,new_graph):
    exgraph= visualize_graph(prev_graph)
    ngraph= visualize_graph(new_graph)
    graph_page= ttk.Frame(window, width= 1000, height=900)
    graph_page.pack_propagate(False)

    prev_label= ttk.Label(graph_page,text='Previous Graph', font=("Times New Roman", 18 , "bold"))
    prev_label.place(x=135, y=50)
    canvas1 = FigureCanvasTkAgg(exgraph, master=graph_page)
    canvas1.draw()
    canvas1.get_tk_widget().place(x=50, y=100, width=400, height=400)

    curr_label= ttk.Label(graph_page,text='Current Graph', font=("Times New Roman", 18 , "bold"))
    curr_label.place(x=585, y=50)
    canvas2 = FigureCanvasTkAgg(ngraph, master=graph_page)
    canvas2.draw()
    canvas2.get_tk_widget().place(x=450, y=100, width=400, height=400)

    back_button= ttk.Button(graph_page, text= 'Back', command= lambda: return_to_back(graph_page, result_page) )
    back_button.place(x=400,y=600 ,width=100, height=35)

    result_page.pack_forget()
    graph_page.pack()

def balances(graph,friend_list):
    balance_dict={friend:0 for friend in friend_list}
    for ch in graph:
        for key in graph[ch]:
            balance_dict[ch]-=graph[ch][key]
            balance_dict[key]+= graph[ch][key]
    balance_page= ttk.Frame(window, width= 700, height= 700)
    balance_page.pack_propagate(False)
    bal_table= ttk.Treeview(balance_page, columns= ('number', 'name', 'balance'), show='headings')
    bal_table.heading( 'number', text= 'Number')
    bal_table.heading('name', text='Name')
    bal_table.heading('balance', text='Balance')
    bal_table.column('number', width=150)
    bal_table.column('name', width=150)
    bal_table.column('balance', width=150)
    i=1
    for key,value in balance_dict.items():
        number=i
        name=key
        balance='{:0.2f}'.format(value)
        i+=1
        bal_table.insert(parent='', index=tk.END, values=(number,name,balance))
    bal_table.pack()

    back_button= ttk.Button(balance_page, text= 'Back', command= lambda: return_to_back(balance_page, result_page) )
    back_button.place(x=300,y=600 ,width=100, height=50)
    result_page.pack_forget()
    balance_page.pack()

def expense_chart(data_frame):
    pass
            

def return_to_back(current_page, back_page):
    current_page.pack_forget()
    back_page.pack()

def expense_detail_func(selected_item, page_to_forget):
    page_to_forget.pack_forget()
    expense_detail_page=ttk.Frame(window, width= 700, height=700)
    expense_detail_page.pack_propagate(False)
    if page_to_forget==expense_list_page:
        path=f"files//{group_nam}_{selected_gtype}.csv"
    else:
        path=file_path
    df=pd.read_csv(path)
    df = df.iloc[:, :-1]
    df = df.set_index(df.columns[0])
    print(selected_item)
    print(list(selected_item))
    number=int(selected_item[0])-1
    selected_line=df.iloc[number, :]
    det=selected_line.name.split('_')
    ex_name=det[0]
    ex_amount=float(det[1])
    ex_type=det[2]
    ex_payer=det[3]
    ex_date=det[5]
    expense_name_label=ttk.Label(expense_detail_page, text=f"Expense name: {ex_name}", font=(8))
    expense_name_label.place(x=100,y=40)

    expense_type_label=ttk.Label(expense_detail_page, text=f"Expense type: {ex_type}", font=(8))
    expense_type_label.place(x=350,y=40)

    expense_payer_label=ttk.Label(expense_detail_page, text=f"Expense payer: {ex_payer}", font=(8))
    expense_payer_label.place(x=100,y=90)

    expense_amount_label=ttk.Label(expense_detail_page, text=f"Expense amount: {ex_amount}", font=(8))
    expense_amount_label.place(x=350,y=90)

    expense_date_label=ttk.Label(expense_detail_page, text=f"Expense date: {ex_date}", font=(8))
    expense_date_label.place(x=220,y=140)

    ex_detail_table=ttk.Treeview(expense_detail_page,columns=('number', 'name', 'share', 'amount'), show='headings')
    ex_detail_table.heading('number',text='Number')
    ex_detail_table.heading('name',text='Name')
    ex_detail_table.heading('share',text='Share')
    ex_detail_table.heading( 'amount',text='Amount')
    ex_detail_table.column('number', width=100)
    ex_detail_table.column('name', width=150)
    ex_detail_table.column('share', width=130)
    ex_detail_table.column('amount', width=130)
    i=1
    for element in selected_line.items():
        num=i
        name=element[0]
        share=element[1]
        amount=float(element[1])*ex_amount
        amount='{:.2f}'.format(amount)
        i+=1
        ex_detail_table.insert(parent='', index= tk.END,values=(num,name,share,amount))
    ex_detail_table.place(x=100,y=200)

    back_button= ttk.Button(expense_detail_page, text= 'Back', command= lambda: return_to_back(expense_detail_page, page_to_forget) )
    back_button.place(x=300,y=600 ,width=100, height=50)
    expense_detail_page.pack()



def on_exitem_select(event):
    global selected_exitem_details
    selected_item = expense_table.focus()
    selected_exitem_details = expense_table.item(selected_item, "values")
    if selected_exitem_details:
        expense_details_button.config(state=tk.NORMAL)

def exon_exitem_select(event):
    global exselected_exitem_details
    selected_item = expense_tabl.focus()
    exselected_exitem_details = expense_tabl.item(selected_item, "values")
    if exselected_exitem_details:
        exexpense_details_button.config(state=tk.NORMAL)


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

group_curr=tk.StringVar(value='IRT')
group_check_box= ttk.Combobox(master= add_group_page ,values=('IRT', 'USDT'), textvariable=group_curr)
group_check_box.place(x=355,y=370, width=90)
group_curr_label=ttk.Label(add_group_page, text="Expense currency")
group_curr_label.place(x=225,y=370)


create_button=ttk.Button(master= add_group_page, text='Create', command= create_group)
create_button.place(x=350,y=430)

main_page_button=ttk.Button(master= add_group_page, text='Main Page', command= lambda: return_to_mainpage(add_group_page))
main_page_button.place(x=335,y=480)
   
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

expense_page1=ttk.Frame(master=window ,width= 800, height=700)
expense_page1.pack_propagate(False)   

expense_page2=ttk.Frame(master=window ,width= 800, height=700)
expense_page2.pack_propagate(False)

error_label8=ttk.Label(master= expense_page1, text='', foreground="red")
error_label9=ttk.Label(master= expense_page2, text='', foreground="red")

def show_guide():
    guide_window = tk.Toplevel(window)
    guide_window.title("Guide")
    guide_window.geometry("900x400")
    
    ttk.Label(guide_window, text="Guide to Input Patterns", font=("Times New Roman", 14, "bold")).pack(pady=10)
    ttk.Label(guide_window, text="1. Name: Must be unique.", font=("Times New Roman", 12)).pack(anchor="w", padx=20)
    ttk.Label(guide_window, text="2. Amount: Must be a number.", font=("Times New Roman", 12)).pack(anchor="w", padx=20)
    ttk.Label(guide_window, text="3. Payer: Must be a member of the group.", font=("Times New Roman", 12)).pack(anchor="w", padx=20)
    ttk.Label(guide_window, text="4. Owers : Must be a list of commma seperated names which each ower must be a member of the group .", font=("Times New Roman", 12)).pack(anchor="w", padx=20)
    ttk.Label(guide_window, text="5. Shares : Must contain a list of comma seperated values which the first value corresponds to the payer and\n \
               the rest of the values represent the share of the owers with the order enetered in owers list", font=("Times New Roman", 12)).pack(anchor="w", padx=20)
    ttk.Label(guide_window, text="6. Date: Must follow this pattern mm/dd/yyyy and must be based on Christian calendar,\n the default value is the current date .", font=("Times New Roman", 12)).pack(anchor="w", padx=20)
  
    ttk.Button(guide_window, text="Close", command=guide_window.destroy).pack(pady=20)

def expense_stuffs(expense_page):
    
    question_mark = ttk.Label(expense_page, text="❓ Guide", foreground="blue", cursor="hand2")
    question_mark.place(x=5, y=10)
    question_mark.bind("<Button-1>", lambda e: show_guide())

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

    recurrency_type=tk.StringVar()
    check_box= ttk.Combobox(master= expense_page, state=tk.DISABLED ,values=("Daily", "Weekly", "Monthly", "Yearly"), textvariable=recurrency_type)
    check_box.place(x=245,y=585, width=90)

    recurrent_bin=tk.StringVar(value='no')
    recurrent_y= ttk.Radiobutton(master= expense_page, variable= recurrent_bin, value='yes', text='Recurring', command= lambda: is_recurrent(recurrent_bin, check_box, recurrency_type) )
    recurrent_n= ttk.Radiobutton(master= expense_page, variable= recurrent_bin, value='no', text='Non-recurring', command= lambda: is_recurrent(recurrent_bin, check_box, recurrency_type) )
    recurrent_y.place(x=0,y=590)
    recurrent_n.place(x=100,y=590)

    
    expense_date=tk.StringVar(value=today)
    expense_date_entry=ttk.Entry(expense_page, textvariable= expense_date)
    expense_date_entry.place(x=460,y=590, width=100)
    expense_date_label=ttk.Label(expense_page, text="Expense date")
    expense_date_label.place(x=360,y=590)

    expense_curr=tk.StringVar(value='IRT')
    curr_check_box= ttk.Combobox(master= expense_page ,values=('IRT', 'USDT'), textvariable=expense_curr)
    curr_check_box.place(x=710,y=590, width=90)
    expense_curr_label=ttk.Label(expense_page, text="Expense currency")
    expense_curr_label.place(x=590,y=590)


    main_page_button=ttk.Button(master= expense_page, text='Main Page', command= lambda: return_to_mainpage(expense_page))
    main_page_button.place(x=335,y=650)

    added_expense_button=ttk.Button(master= expense_page, text='Add', command= lambda : return_expense_list(expense_page,expense_name, expense_amount, expense_payer, expense_owers, selected_extype, split_type, expense_share,recurrency_type,expense_date,expense_curr))
    added_expense_button.place(x=270,y=650)

def is_recurrent(recurr_state, ch_box, rec_type):
    if recurr_state.get()=='yes':
        ch_box.config( state=tk.NORMAL)
    else:
        rec_type.set(value="")
        ch_box.config(state=tk.DISABLED)

expense_list_page=ttk.Frame(master=window, width= 700, height=700)
expense_list_page.pack_propagate(False)

expense_table_frame=ttk.Frame(master=expense_list_page,width=300, height=400)
expense_table_frame.place(x=50, y=100)

main_page_button=ttk.Button(master= expense_list_page, text='Main Page', command= lambda: return_to_mainpage(expense_list_page))
main_page_button.place(x=335,y=600)

add_expense_button=ttk.Button(master= expense_list_page, text='Add Expenses', command= lambda: expense_page_func(expense_list_page,expense_page1)  )
add_expense_button.place(x=300,y=550)

expense_details_button= ttk.Button(master= expense_list_page, state=tk.DISABLED ,text='Details', command= lambda: expense_detail_func(selected_exitem_details,expense_list_page)  )
expense_details_button.place(x=345,y=400)

calculate_button=ttk.Button(master= expense_list_page, text='Caluclate Transactions', command= lambda: calculate_trans(expense_list_page, f"files//{group_nam}_{selected_gtype}.csv" ) )
calculate_button.place(x=300,y=500)

search_var = tk.StringVar()
search_bar = ttk.Entry(expense_list_page, textvariable=search_var, width=20)
search_bar.place(x=280, y=10)

search_button = ttk.Button(expense_list_page, text="Search", command=lambda : search_items(f"files//{group_nam}_{selected_gtype}.csv"))
search_button.place(x=400, y=10)

reset_button = ttk.Button(expense_list_page, text="Reset", command= lambda : reset_search(f"files//{group_nam}_{selected_gtype}.csv"))
reset_button.place(x=480, y=10)

#existing group expenses
exexpense_list_page=ttk.Frame(master=window, width= 700, height=700)
exexpense_list_page.pack_propagate(False)

expense_tabl_frame=ttk.Frame(master=exexpense_list_page,width=200, height=400)
expense_tabl_frame.place(x=50, y=100)

main_page_button=ttk.Button(master= exexpense_list_page, text='Main Page', command= lambda: return_to_mainpage(exexpense_list_page))
main_page_button.place(x=335,y=550)

add_expense_button=ttk.Button(master= exexpense_list_page, text='Add Expenses', command= lambda: expense_page_func(exexpense_list_page,expense_page2)  )
add_expense_button.place(x=330,y=500)

exexpense_details_button= ttk.Button(master= exexpense_list_page, state=tk.DISABLED ,text='Details', command= lambda: expense_detail_func(exselected_exitem_details,exexpense_list_page)  )
exexpense_details_button.place(x=345,y=400)

excalculate_button=ttk.Button(master= exexpense_list_page, text='Caluclate Transactions', command= lambda: calculate_trans(exexpense_list_page, file_path)  )
excalculate_button.place(x=300,y=450)

exsearch_var = tk.StringVar()
exsearch_bar = ttk.Entry(exexpense_list_page, textvariable=exsearch_var, width=20)
exsearch_bar.place(x=280, y=10)

exsearch_button = ttk.Button(exexpense_list_page, text="Search", command= lambda : search_items(file_path))
exsearch_button.place(x=400, y=10)

exreset_button = ttk.Button(exexpense_list_page, text="Reset", command= lambda : reset_search(file_path))
exreset_button.place(x=480, y=10)

result_page=ttk.Frame(window, width= 700, height=700)
result_page.pack_propagate(False)

main_page_button=ttk.Button(master= result_page, text='Main Page', command= lambda: return_to_mainpage(result_page))
main_page_button.place(x=300,y=600)



window.mainloop()
