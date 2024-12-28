import numpy as np
import heapq as hq
from datetime import date
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.pyplot as plt


class Group():
    def __init__(self, group_name, group_type):
        self.expenses = []
        self.friends = []
        self.groups = {} #key : gr name, value : category
        self.name = group_name
        self.type = group_type
        self.group_graph = []

    def add_friend(self, new_friend):
        self.friends.append(new_friend)

    def add_expense(self, expense):
        self.expenses.append(expense)
        expense.calculate_shares()
        self.day = date.today()
        self.group_graph += expense.graph
        if expense.group_name not in self.groups:
            self.groups[expense.group_name] = expense.category
        self.update_pay(expense)

    def update_pay(self, expense):
        for i, person in enumerate(expense.owers):
            if person != expense.payer:
                self.friends[person].money -= expense.for_one[i]
                self.friends[expense.payer].money += expense.for_one[i]

    def all_groups(self):
        return [group for group in self.groups]

    def expenses_in_gr(self, group):
        return [expense for expense in self.expenses if expense.group_name == group]

    def expenses_in_cat(self, category):
        return [expense for expense in self.expenses if expense.category == category]

    def total_gr(self, group):
        e = self.expenses_in_gr(group)
        e_amount = [ex.value for ex in e]
        return sum(e_amount)

    def total_cat(self, category):
        e = self.expenses_in_cat(category)
        e_amount = [ex.value for ex in e]
        return sum(e_amount)

    def total_person(self, person):
        e_person = [expense for expense in self.expenses if expense.payer == person or person in expense.owers]
        e_person_amount = []
        for ex in e_person:
            if ex.payer == person:
                person_ind = 0
            else:
                person_ind = ex.owers.index(person) + 1
            e_person_amount.append(ex.value * (ex.shares_dict[person_ind] / ex.value)
        return sum(e_person_amount)

    def search_person(self, person):
        return [expense for expense in self.expenses if expense.payer == person or person in expense.owers]

    def search_date(self, search_day):
        return [expense for expense in self.expenses if expense.day == search_day]

def total_person_balance(graph, person):
    return graph[person]

class Friend():
    def __init__(self, name):
        self.name = name
        self.money = 0


class Expense():
    ALLOWED_CATEGORIES = ("House", "Food", "Shopping", "Transportation", "Hobby", "Medicine", "Education", "Gifts", "Business", "Pets", "Charity")
    ALLOWED_PAYMENT_METHOD = ("cash", "credit_cards")
    ALLOWED_SPLIT_TYPE = ('equal', 'percentage', 'exact')
    # payment methods = online -> show شماره کارت or لینک پرداخت از آپ, cash

    def __init__(self, name, value, payer, owers, group_name, category, payment_method, split_type = 'equal', shares = None):
        self.name = name
        self.value = value
        self.payer = payer
        self.owers = owers
        self.shares = shares
        self.split_type = split_type
        self.group_name = group_name
        self.category = category
        self.payment_method = payment_method
        self.day = None
        self.for_one = []
        self.graph = []
        self.shares_dict = {}

    def calculate_shares(self):
        if self.split_type == 'equal':
            self.shares = [1] * (len(self.owers) + 1)
            total_shares = sum(self.shares)
            self.for_one = [self.value * self.shares[i] / total_shares for i in range(len(self.shares))]
        else:
            if self.shares:
                total_shares = sum(self.shares)
                self.for_one = [self.value * self.shares[i] / total_shares for i in range(len(self.shares))]

    def shares_to_dict(self):
        self.calculate_shares()
        self.shares_dict[self.payer] = self.for_one[0]
        for i, ower in enumerate(self.owers):
            self.shares_dict[ower] = self.for_one[i+1]

    def to_graph(self):
        for i, ower in enumerate(owers):
            self.graph.append([self.payer, ower, self.for_one[i+1]])
        return self.graph
# an example to show if visualization works
expense_1 = Expense(
    name ="Diner",
    value =300,
    payer="Maryam",
    owers = ["Manouchehr", "Jalil"],
    group_name="family", category= 'Food', payment_method="cash", split_type='exact', shares=[1,2,3])

expense_2 = Expense(
    name ="Cinema",
    value =100,
    payer="Manouchehr",
    owers = ["Zahra", "Jalil"],
    group_name="family", category= 'Hobby', payment_method="cash", split_type='percentage', shares=[0.25,0.5,0.25])

expense_3 = Expense(
    name ="Tax",
    value =60,
    payer="Zahra",
    owers = ["Maryam", "Jalil"],
    group_name="family", category= 'House', payment_method="credit_cards", split_type='exact', shares=[1,1,1])

# List of expenses
expenses = [expense_1, expense_2, expense_3]
for expense in expenses:
    expense.shares_to_dict()


# graph visualization
def calculate_color(graph):
    node_colors = []
    for node in graph.nodes:
        outgoing = sum(graph[u][v]['weight'] for u, v in graph.out_edges(node))
        incoming = sum(graph[u][v]['weight'] for u, v in graph.in_edges(node))
        if outgoing > incoming:
            node_colors.append('red')  # Debtor
        else:
            node_colors.append('green')  # Creditor
    return node_colors

def visualize_graph(graph):
    vis_graph = nx.DiGraph()
    for payer, owers in graph.items():
        for ower, amount in owers.items():
            vis_graph.add_edge(payer, ower, weight = amount)
    nodes_pos = nx.spring_layout(vis_graph, k = 5, iterations=50)
    nodes_color = calculate_color(vis_graph)
    plt.figure(figsize = (8, 6))
    nx.draw(vis_graph, nodes_pos, with_labels= True, node_color = nodes_color, node_size = 1000, font_size = 10)
    nx.draw_networkx_edges(vis_graph, nodes_pos, arrowsize=15)
    edge_labels = nx.get_edge_attributes(vis_graph, 'weight')
    nx.draw_networkx_edge_labels(vis_graph, nodes_pos, edge_labels=edge_labels)
    plt.show()

print(graph)
visualize_graph(graph)

# Total debts visualization by Pie chart

def total_debts(garph):
    total_debts = {}
    for payer, ower in graph.items():
        for ower, amount in ower.items():
            total_debts[payer] = total_debts.get(payer, 0) + amount
    return total_debts

def visualize_pie_chart(total_debts):
    labels = total_debts.keys()
    values = total_debts.values()
    # different colors for different people
    colors = plt.cm.tab20(np.linspace(0, 1, len(values)))
    plt.figure(figsize=(8, 6))
    plt.pie(values, labels=labels, colors=colors)
    plt.title('Portion of everyone in Unpaid debts')
    plt.show()

visualize_pie_chart(total_debts(graph))


# Chart of shares
def generate_colors(expenses):
    all_people = set(person for expense in expenses for person in expense.shares_dict.keys())
    return {person: (random.random(), random.random(), random.random()) for person in all_people}

def visualize_bar_chart(expenses):
    fig, ax = plt.subplots(figsize = (8, 6))
    colors = generate_colors(expenses)
    bar_pos = range(len(expenses))
    for i, expense in enumerate(expenses):
        # start to draw a bar
        first_height = 0
        for person, share in expense.shares_dict.items():
            height_for_now = expense.shares_dict[person]
            ax.bar(bar_pos[i], bottom = first_height, label = person if i == 0 else "", height= height_for_now, color= colors[person])
            ax.text(i, first_height + height_for_now / 2, person, ha="center", va="center", fontsize=10, color="white", fontweight="bold")
            first_height += height_for_now
        ax.text(bar_pos[i], expense.value + 5, expense.payer, ha='center', fontsize=10, color='black')

    all_people = set(person for expense in expenses for person in expense.shares_dict.keys())
    ax.set_title("Expenses Shares Bar Chart", fontsize=16)
    ax.set_ylabel("Amount", fontsize=12)
    ax.set_xlabel("Expenses", fontsize=12)
    ax.set_xticks(bar_pos)
    ax.set_xticklabels([f"Expense {expense.name}" for i in bar_pos])
    ax.legend(handles= [plt.Line2D([1], [1], linewidth= 5, color = colors[person]) for person in all_people], labels= all_people, title="Participants", loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()


visualize_bar_chart(expenses)