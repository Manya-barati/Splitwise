import datetime
import requests
from datetime import datetime
import numpy as np
import heapq as hq
from datetime import date, timedelta
import random
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

API_KEY = "7790bd062ddc4e368a338a0c7cd596cb"
API_URL = "https://openexchangerates.org/api/latest.json"
key_nob = "f053a43d8e465fde3f46b6fee95405f34b6f8e3c"
url_nob = "https://api.nobitex.ir/market/stats"


class CurrencyConversion:
    def __init__(self, api_url, api_key, nob_key, nob_url):
        self.api_url = api_url  # openexchange
        self.api_key = api_key
        self.nob_key = nob_key  # nobitex
        self.nob_url = nob_url
        self.exchange_rates = {}
        self.historical_rates = {}  # if the expense is not for today

    def get_rates(self):
        # getting exchange rates from nobitex website for today
        try:
            output = requests.post(self.nob_url, json={})
            # only if output = 200 it has been gone without error
            if output.status_code == 200:
                data = output.json()
                self.exchange_rates = {market: float(info.get('latest', 0)) for market, info in data['stats'].items()}
                # check for rial if toman is not available
                if "usdt-rls" in self.exchange_rates and "usdt-irt":
                    self.exchange_rates["usdt-irt"] = self.exchange_rates["usdt-rls"] / 10
                else:
                    # if usdt conversion to no rial and no toman was in the database
                    print("Tether to Rial rate is Not Supported")
            else:
                # if the api request cause error
                print(f"Error: {output.status_code},{output.text}")
        except Exception as e:
            print(f"Error: {e}")

    # getting exchange rates from nobitex website for not today
    def get_historical_rates(self, symbol, resolution, from_date, to_date):
        try:
            # from_timestamp and to_timestamp are defined to be used in parameters of nobitex input (seconds passed from 1970-01-01)
            from_timestamp = int(datetime.strptime(from_date, "%Y-%m-%d").timestamp())
            to_timestamp = int(datetime.strptime(to_date, "%Y-%m-%d").timestamp())
            # parameters needed for nobitex request
            params = {
                "symbol": symbol,  # "IRT" for ex
                "resolution": resolution,  # D stands for daily for ex
                "from": from_timestamp,
                "to": to_timestamp,
            }
            output = requests.get("https://api.nobitex.ir/market/udf/history", params=params)
            if output.status_code == 200:
                data = output.json()
                if data.get("s") == "ok":
                    # without error
                    return data
                else:
                    print(f"Error in historical data response: {data}")
                    return {}
            else:
                print(f"Error fetching historical rates: {output.status_code}, {output.text}")
                return {}
        except Exception as e:
            print(f"Error fetching historical rates: {e}")
            return {}

    def convert_currency(self, value, from_curr, to_curr, exp_date):
        if exp_date and exp_date != str(date.today()):
            yesterday = (datetime.strptime(exp_date, '%Y-%m-%d').date() - timedelta(days=1)).strftime(
                '%Y-%m-%d')  # calculating yesterday to use as to date
            historical_data = self.get_historical_rates("USDTIRT", "D", yesterday, exp_date)
            if historical_data:
                # read the exchange rate for usdt to irt
                self.exchange_rates["usdt-irt"] = historical_data["c"][-1]
        else:
            # for today just get rates
            self.get_rates()
        if from_curr == to_curr:
            return value
        from_curr = from_curr.lower()
        to_curr = to_curr.lower()
        market = f"{from_curr}-{to_curr}"
        anti_market = f"{to_curr}-{from_curr}"
        # if usdt to irt is not available just use 1/ irt to usdt
        if market not in self.exchange_rates:
            if anti_market in self.exchange_rates:
                self.exchange_rates[market] = 1 / self.exchange_rates[anti_market]
                rate = self.exchange_rates[market]
            else:
                raise ValueError(f"Market pair {market} is not supported.")
        else:
            # the rates needed was available
            rate = self.exchange_rates[market]
        return value * rate


# get rates to be ready!
curr_convertor = CurrencyConversion(api_url=API_URL, api_key=API_KEY, nob_key=key_nob, nob_url=url_nob)
curr_convertor.get_rates()
# an example to check the exchanging
'''try:
    converted_value = curr_convertor.convert_currency(1, 'USDT', 'irt', exp_date="2023-12-02")
    print(f"Converted value: {converted_value} IRT", " 2024 ")
except ValueError as e:
    print(e)
try:
    converted_value = curr_convertor.convert_currency(1, 'USDT', 'IRT', exp_date="2025-01-03")
    print(f"Converted value: {converted_value} IRT", "2025")
except ValueError as e:
    print(e)'''


class Group():
    def __init__(self, group_name, group_type):
        self.expenses = []
        self.friends = []
        self.name = group_name
        self.type = group_type
        self.group_graph = []

    # add member to a group
    def add_friend(self, new_friend):
        self.friends.append(new_friend)

    # add expense to a group
    def add_expense(self, exp):
        self.expenses.append(exp)
        # change date input (str) to date object
        exp.calculate_date()
        # convert currency if input and output curr is different
        exp.convert_curr()
        # each time adding a expense, check for the recurring expenses
        self.recurring_expense()

    # def update_pay(self, expense):
    #    for i, person in enumerate(expense.owers):
    #        if person != expense.payer:
    #            self.friends[expense.owers.index(person)].money -= expense.for_one[i]
    #            self.friends[expense.owers.index(expense.payer)].money += expense.for_one[i]

    #
    def recurring_expense(self):
        today = date.today()
        # if next occurance of the expense has already past or its today
        for expense in self.expenses:
            if expense.recurring and expense.next <= today:
                new_expense = Expense(name=expense.name, value=expense.value, payer=expense.payer, owers=expense.owers,
                                      group_name=expense.group_name, category=expense.category, split_type='equal',
                                      shares=None,
                                      recurring=True, interval=expense.interval)
                self.add_expense(new_expense)
                expense.next = new_expense.calculate_next()

    # all expenses in a category
    def expenses_in_cat(self, category):
        return [expense for expense in self.expenses if expense.category == category]

    # total of expenses in a group
    def total_gr(self):
        e_amount = [ex.value for ex in self.expenses]
        return sum(e_amount)

    # total of expenses in a category
    def total_cat(self, category):
        e = self.expenses_in_cat(category)
        e_amount = [ex.value for ex in e]
        return sum(e_amount)

    # total of expense values in which person was present
    def total_person(self, person):
        e_person = [expense for exp in self.expenses if expense.payer == person or person in expense.owers]
        e_person_amount = []
        return sum(e_person_amount)

    def search_person(self, person):
        return [expense for expense in self.expenses if expense.shares[person]]

    def search_date(self, search_day):
        return [expense for expense in self.expenses if expense.day == search_day]

    # values spent on each category
    def expense_in_category(self):
        all_cat = {category: 0 for category in Expense.ALLOWED_CATEGORIES}
        for ex in self.expenses:
            if ex.category in all_cat:
                all_cat[ex.category] += expense.value
        return all_cat


class Friend():
    def __init__(self, name):
        self.name = name
        self.money = 0


class Expense:
    ALLOWED_CATEGORIES = ("House", "Food", "Shopping", "Transportation", "Hobby", "Medicine", "Education", "Gifts",
                          "Business", "Pets", "Charity")
    ALLOWED_SPLIT_TYPE = ('equal', 'percentage', 'exact')
    ALLOWED_INTERVALS = ("Daily", "Weekly", "Monthly", "Yearly")

    def __init__(self, name, value, payer, owers, group_name, category, ex_date, currency, output_curr, split_type,
                 shares, recurring=False, interval=None):
        self.name = name
        self.value = value
        self.payer = payer
        self.owers = owers
        self.shares = shares
        self.split_type = split_type
        self.group_name = group_name
        self.category = category
        self.currncy = currency if currency else "IRT"
        self.out_curr = output_curr if output_curr else "IRT"
        self.day = ex_date if ex_date else date.today()
        self.recurring = recurring
        self.interval = interval
        self.next = self.calculate_next()
        self.for_one = []
        self.graph = []

    # convert currency if needed
    def convert_curr(self):
        if self.currncy != self.out_curr:
            if isinstance(self.day, str):
                self.day = datetime.strptime(self.day, '%Y-%m-%d').date()
            date_str = self.day.strftime('%Y-%m-%d')
            self.value = curr_convertor.convert_currency(self.value, self.currncy, self.out_curr, exp_date=date_str)

    # convert date from str to date object
    def calculate_date(self):
        if isinstance(self.day, str):  # check if input date is str
            self.day = datetime.strptime(self.day, "%Y-%m-%d").date()

    '''# calculate shares of everyone
    def calculate_shares(self):
        if self.split_type == 'equal':
            self.shares = [1] * (len(self.owers) + 1)
            total_shares = sum(self.shares)
            self.for_one = [self.value * self.shares[i] / total_shares for i in range(len(self.shares))]
        else:
            if self.shares:
                total_shares = sum(self.shares)
                self.for_one = [self.value * self.shares[i] / total_shares for i in range(len(self.shares))]'''

    # calculate next due of recurring expenses
    def calculate_next(self):
        if self.recurring and self.interval:
            if self.interval == 'daily':
                return self.day + timedelta(days=1)
            if self.interval == 'weekly':
                return self.day + timedelta(weeks=1)
            if self.interval == 'monthly':
                return self.day + timedelta(days=30)
            if self.interval == 'yearly':
                return self.day + timedelta(days=365)
            return None

    # convert shares list to dict : items = people, values = amounts
    '''def shares_to_dict(self):
        people = [self.payer] + self.owers
        print(people)
        self.shares_dict = {person: share for (person, share) in zip(people, self.shares)}'''

    # changing the structure of a dict to a list of lists (like transactions)
    def to_graph(self):
        for i, ower in enumerate(self.owers):
            self.graph.append([self.payer, ower, self.for_one[i + 1]])
        return self.graph


# balance of anybody
def total_person_balance(graph, person):
    return graph[person]


# total values of all expenses in which person was present (separated by category)
def exp_for_one_in_cat(group_list, person):
    for group in group_list:
        exp_for_person = group.search_person(person)
    all_cat = {category: 0 for category in Expense.ALLOWED_CATEGORIES}
    for exp in exp_for_person:
        if exp.category in all_cat:
            all_cat[exp.category] += exp.value
    return all_cat


# Create class (group and expense instances) from excel file (output of graphics part)
def CreateCalss(file_path, out_curr):
    # read the csv file as a dataframe
    data = pd.read_csv(file_path)
    data = data.iloc[:, :-1]
    print(data)

    # read the name and type of the group from its file path
    file_name = file_path.split('\\')[-1]  # last is the file name
    group_name, group_type = file_name.split('_')[0], file_name.split('_')[1].split('.')[0]
    print(group_name, group_type)

    # make a group
    group = Group(group_name, group_type)

    # read the group members as a list from col names (except first col)
    people = list(data.columns[1:])

    # adding people to group
    for person in people:
        group.add_friend(Friend(person))

    # read each row
    for _, row in data.iterrows():
        # split first col of each row
        class_attributes = row.iloc[0].split('_')
        name, value, category, payer, recurrent, exp_date, in_curr = class_attributes

        # set the types
        value = float(value)
        recurrent_options = ['Daily', 'Monthly', 'Weekly', 'Yearly']
        recurrent_mode = True if recurrent in recurrent_options else False
        exp_date = exp_date.strip('"')
        exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()

        # read the shares as a list
        shares_list = list(row.iloc[1:])
        owers = [people[i] for i, share in enumerate(shares_list) if share > 0]
        shares_dict = {person:share for (person, share) in zip(people,shares_list) if share > 0}
        print(shares_dict)

        # creating instances of Expense class
        expense = Expense(name=name, value=value, payer=payer, owers=owers, group_name=group_name, category=category,
                          ex_date=exp_date, split_type='exact', shares=shares_dict, recurring=recurrent_mode,
                          interval=recurrent, currency=in_curr, output_curr=out_curr)

        # adding expense to the group
        group.add_expense(expense)

    return group


'''expense_1 = Expense(name ="Diner", value =300, payer="Maryam", ex_date = "2025-01-01", owers = ["Manouchehr", "Jalil"], group_name="family",
                        category= 'Food', payment_method="cash", split_type='exact', shares=[1,2,3])

expense_2 = Expense(
    name ="Cinema", value =100, payer="Manouchehr", ex_date = None, owers = ["Zahra", "Jalil"], group_name="family", category= 'Hobby',
    payment_method="cash", split_type='percentage', shares=[0.25,0.5,0.25])

expense_3 = Expense(
    name ="Tax",
    value =60,
    payer="Zahra", ex_date = "2025-01-01",
    owers = ["Maryam", "Jalil"],
    group_name="family", category= 'House', payment_method="credit_cards", split_type='exact', shares=[1,1,1])

expense_4 = Expense(name ="ABC", value =400, payer="Maryam", ex_date = "2024-12-28", owers = ["Manouchehr", "Jalil", "Roya"],
                    group_name="D", category= 'Business', payment_method="cash", split_type='exact', shares=[1,2,3,4])'''

'''# List of expenses
expenses = [expense_1, expense_2, expense_3, expense_4]
for ex in expenses:
    ex.calculate_date()
graph = {'A': {'B': 100, 'C': 200}, 'B': {'D': 150}, 'C': {}, 'D': {'A': 50}}

for expense in expenses:
    expense.shares_to_dict()'''

gr = CreateCalss('files\\ccc_Family.csv', 'IRT')
print(gr.expenses[1].shares, gr.expenses[1].shares)


# cenrtrality calculation
def graph_to_network(graph):
    Graph = nx.DiGraph()
    for payer, owers in graph.items():
        for ower, amount in owers.items():
            Graph.add_edge(payer, ower, weight=amount)
    return Graph


# calculate degree centrality
def degree_cent(Graph):
    return nx.degree_centrality(Graph)


# calculate betweenness centrality
def between_cent(Graph):
    return nx.betweenness_centrality(Graph)


# calculate closeness centrality
def close_cent(Graph):
    return nx.closeness_centrality(Graph)


# calculate eigenvector centrality
def eigen_cent(Graph):
    return nx.eigenvector_centrality(Graph)


# graph visualization
def calculate_color(graph, central_node):
    node_colors = {}
    balance = {}
    for node in graph.nodes:
        outgoing = sum(graph[u][v]['weight'] for u, v in graph.out_edges(node))
        incoming = sum(graph[u][v]['weight'] for u, v in graph.in_edges(node))
        balance[node] = outgoing - incoming
    for node in graph.nodes:
        if node == central_node:
            node_colors[node] = 'purple'  # Mother of Expenses (based on centrality)
        elif balance[node] == max(balance.values()):
            node_colors[node] = 'yellow'  # Avizoon
        elif balance[node] > 0:
            node_colors[node] = 'red'  # Debtor
        elif balance[node] < 0:
            node_colors[node] = 'green'  # Creditor
        else:
            node_colors[node] = 'blue'  # balance = 0
    return node_colors


# graph visualization using networkx
def visualize_graph(graph):
    # making a directional graph
    vis_graph = nx.DiGraph()

    # adding edges to graph
    for payer, owers in graph.items():
        for ower, amount in owers.items():
            vis_graph.add_edge(payer, ower, weight=amount)

    # determining position of nodes
    nodes_pos = nx.spring_layout(vis_graph, k=5, iterations=50)

    # using color of nodes calculated before
    nodes_color = calculate_color(vis_graph)
    node_color = [nodes_color[node] for node in vis_graph.nodes]

    # visualization
    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(vis_graph, nodes_pos, with_labels=True, node_color=node_color, node_size=1000, font_size=10)
    nx.draw_networkx_edges(vis_graph, nodes_pos, arrowsize=15, ax=ax)
    edge_labels = nx.get_edge_attributes(vis_graph, 'weight')
    nx.draw_networkx_edge_labels(vis_graph, nodes_pos, edge_labels=edge_labels, ax=ax)

    # legend making (drawing lines in the colors needed)
    legend_elements = [plt.Line2D([1], [1], color='green', linewidth=4, label='Creditor'),
                       plt.Line2D([1], [1], color='red', linewidth=4, label='Debtor'),
                       plt.Line2D([1], [1], color='yellow', linewidth=4, label='Avizoon'),
                       plt.Line2D([1], [1], color='purple', linewidth=4, label='Mother of Expenses'),
                       plt.Line2D([1], [1], color='blue', linewidth=4, label='No Need to Pay')]
    ax.legend(handles=legend_elements, loc='upper right', title="Legend")

    return fig


# Total debts visualization by Pie chart
def total_debts(graph):
    total_debts = {}
    # a dict of how much of total unpaid debts belong to anyone
    for payer, ower in graph.items():
        for ower, amount in ower.items():
            total_debts[payer] = total_debts.get(payer, 0) + amount
    return total_debts


# visualization of pie chart
def visualize_pie_chart(total_debts):
    labels = total_debts.keys()
    values = total_debts.values()
    # different colors for different people
    colors = plt.cm.tab20(np.linspace(0, 1, len(values)))
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%")  # autopct is to show percentage
    ax.set_title('Portion of everyone in Unpaid debts')
    return fig


# Chart of shares
def generate_colors(expenses):
    # generate unique colors for people
    all_people = set(person for expense in expenses for person in expense.shares.keys())
    return {person: (random.random(), random.random(), random.random()) for person in all_people}


# visualiztion of a bar chart (each bar is for a expense in which person was present showing eveuones shares by colors)
def visualize_bar_chart(group_list, person):
    exp_for_person = []
    for group in group_list:
        # listing all expenses in which person was present
        exp_for_person.extend(group.search_person(person))
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = generate_colors(exp_for_person)
    # calculating position of bars in the plot
    bar_pos = range(len(exp_for_person))

    for i, expense in enumerate(exp_for_person):
        # start to draw a bar
        first_height = 0
        for person, share in expense.shares.items():
            height_for_now = expense.shares[person] * expense.value
            # drawing a bar from start height with height = height_for_now (showing share of that person)
            ax.bar(bar_pos[i], bottom=first_height, label=person if i == 0 else "", height=height_for_now,
                   color=colors[person])
            # showing name of the person on the middle of his/her share
            ax.text(i, first_height + height_for_now / 2, person, ha="center", va="center", fontsize=10, color="white",
                    fontweight="bold")
            # setting start heigh of the next share
            first_height += height_for_now
        ax.text(bar_pos[i], expense.value + 5, expense.payer, ha='center', fontsize=10, color='black')

    all_people = set(person for exp in exp_for_person for person in exp.shares.keys())
    ax.set_title("Expenses Shares Bar Chart", fontsize=16)
    ax.set_ylabel("Amount", fontsize=12)
    ax.set_xlabel("Expenses", fontsize=12)
    ax.set_xticks(bar_pos)
    ax.set_xticklabels([f"Expense {exp.name}" for exp in exp_for_person])
    ax.legend(handles=[plt.Line2D([1], [1], linewidth=5, color=colors[person]) for person in all_people],
              labels=all_people, title="Participants", loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    return fig


# pie chart for all expenses by category (value)
def visualize_expenses_in_category(group):
    # dict of { cat : sum(all expenses in the cat)}
    category_totals = group.expense_in_category()
    labels = [key for key, value in category_totals.items() if value > 0]  # categories
    values = [value for value in category_totals.values() if value > 0]  # total values of categories
    # generation of unrepeated colors for each category
    colors = plt.cm.tab20(np.linspace(0, 1, labels))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.set_title("expenses in each category (total value of each category)")

    return fig


# pie chart for each person expenses by category (value)
def visualize_expenses_for_person(group_list, person):
    # category total of all expenses in which the person was present
    person_category_totals = exp_for_one_in_cat(group_list, person)
    print(person_category_totals)
    labels = [key for key, value in person_category_totals.items() if value > 0]  # category
    values = [value for value in person_category_totals.values() if value > 0]  # total values of cat
    # generation of unrepeated colors for each category
    colors = plt.cm.tab20(np.linspace(0, 1, len(labels)))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.set_title(f"expenses of {person} in each category (total value of each category)")
    return fig


# bar chart for last week (for a single group)
# 1. separating expenses of each day
def each_day_exp(gr_list, person):
    exp_in_day = {}
    for gr in gr_list:
        for exp in gr.expenses:
            for n in range(1, 8):  # change the range (8 = days + 1) if you want more days :) # not preferred :)
                if exp.payer == person or person in exp.owers:
                    today = date.today()
                    day = today - timedelta(days=n)
                    if exp.day == day:
                        if day not in exp_in_day:
                            exp_in_day[day] = {}  # {day: {category : expenses of that day}}
                        if exp.category not in exp_in_day[day]:
                            exp_in_day[day][exp.category] = 0
                        exp_in_day[day][exp.category] += exp.value
    return exp_in_day


# 2. visualize bar chart
def visualize_last_week(gr_list, person):
    exp_in_day = each_day_exp(gr_list, person)  # keys : dates , values : cats in each dates
    print(exp_in_day)
    days = sorted(exp_in_day.keys())  # sorting keys of this dict which are dates
    categories = set(cat for day in exp_in_day.values() for cat in day.keys())  # select all categories present
    cat_colors = {cat: plt.cm.tab20(i / len(categories)) for i, cat in enumerate(categories)}  # set unique colors

    fig, ax = plt.subplots(figsize=(8, 6))
    start_heights = [0] * len(days)

    for category in categories:
        heights = [exp_in_day[day].get(category, 0) for day in days]
        ax.bar([day.strftime("%Y-%m-%d") for day in days], heights, bottom=start_heights, label=category,
               color=cat_colors[category])
        start_heights = [start + height for start, height in zip(start_heights, heights)]

    ax.set_title("Expense trends in last week", fontsize=18)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Total expenses", fontsize=14)
    ax.legend(title="Categories", loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    return fig


'''
gr = Group("test", "Party")
gr.add_expense(expense_1)
gr.add_expense(expense_2)
gr.add_expense(expense_3)
gr.add_expense(expense_4)'''


# save report as pdf
def save_report(graph_before, graph_after, group_list, person):
    pdf_name = "all_visual_reports.pdf"
    with PdfPages(pdf_name) as pdf:
        # first page of pdf report
        plt.title("Graph Before Simplification")
        pdf.savefig(visualize_graph(graph_before))
        plt.title("Graph After Simplification")
        pdf.savefig(visualize_graph(graph_after))

        # second page of pdf report
        pdf.savefig(visualize_last_week(group_list, person))
        pdf.savefig(visualize_bar_chart(group_list, person))

        # third page of pdf report
        pdf.savefig(visualize_pie_chart(total_debts(graph_after)))
        pdf.savefig(visualize_expenses_for_person(group_list, person))


def save_group_report(group):
    with PdfPages("all_visual_reports.pdf") as pdf:
        pdf.savefig(visualize_expenses_in_category(group))

# save_report(graph_1, graph_2, [gr], "Zahra")
pdf_name = "acc_visual_reports.pdf"
with PdfPages(pdf_name) as pdf:
    pdf.savefig(visualize_last_week([gr], 'Manya'))
    pdf.savefig(visualize_bar_chart([gr], 'Manya'))

    # third page of pdf report
    pdf.savefig(visualize_expenses_for_person([gr], 'Manya'))
