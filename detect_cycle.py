import timeit
import heapq as hq
import numpy as np
from scipy.optimize import linprog
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, PULP_CBC_CMD
import random
import networkx as nx

transactions_1= [[0,0,2], [0,1,63], [0,3,85], [0,4,49], [1,1,76], [1,4,27], [2,3,17], [3,0,73], [3,1,32], [3,2,50], [3,3,6], [3,4,71], [4,1,86], [4,4,10]] 
transactions_2 = [['A', 'B', 500], ['B', 'C', 300], ['C', 'D', 200], ['C', 'A', 50], ['D', 'A', 100], ['E', 'F', 400], ['F', 'E', 300]]
transactions_3 = [[0, 1, 10], [0, 1, 10], [0, 2, 20], [1, 2, 5], [1, 3, 10], [2, 3, 15], [1,2,10]]
transactions_4 = [[1, 2, 20], [1, 4, 10], [1, 8, 20], [3, 5, 10], [3, 6, 10], [7, 4, 30], [7, 8, 10], [7, 10, 20], [9, 2, 10], [9, 12, 10], [11, 5, 10]]
# 11 initial transactions, max flow:11 , greedy: 8 
transactions_5 = [[1, 2, 15], [1, 4, 20], [1, 8, 15], [1, 10, 10], [2, 5, 5 ], [2, 12, 10], [3, 5, 5], [3, 6, 5], [3, 10, 10],\
                  [4, 5, 5], [4, 8, 20], [4, 12, 15], [7, 4, 20], [7, 8, 10], [7, 10, 10], [7, 5, 10], [9, 2, 5], [9, 12, 5], [11, 5, 10], [11, 4, 5]]
# 20 initial transactions, max flow: 15, greedy: 9
transactions_6 = [[1, 2, 15], [1, 3, 10], [1, 4, 10], [1, 6, 15], [1, 8, 10], [2, 4, 5], [2, 5, 5], [2, 12, 10], [3, 5, 5], [3, 6, 10], [3, 10, 5]\
                  , [3, 8, 5], [4, 5, 5], [4, 8, 20], [4, 10, 5], [4, 12, 10], [5, 6, 5], [6, 7, 10], [7, 4, 10], [7, 8, 10], [7, 10, 5], \
                    [7, 5, 5], [9, 2, 5], [9, 6, 5], [9, 12, 5], [11, 5, 10], [11, 4, 5]]


class Construct_graph():
    def __init__(self, transactions):
        self.transactions = transactions

    
    def construct_transaction_dict(self):
        self.trans_dict= {}
        for giver, reciever, a in self.transactions:
            if giver not in self.trans_dict.keys():
                self.trans_dict[giver]= len(self.trans_dict)
            if reciever not in self.trans_dict.keys():
                self.trans_dict[reciever]= len(self.trans_dict)

        self.n = len(self.trans_dict)
        self.reverse_trans_dict = {i:j for j, i in self.trans_dict.items()}


    # convert the transactions list to a dictionary
    def convert_to_dict_graph(self):
        dict_graph= {}
        for giver, reciever, amount in self.transactions:
            if giver not in dict_graph:
                dict_graph[giver]= {reciever:amount}
            else:
                if reciever in dict_graph[giver].keys():
                    dict_graph[giver][reciever] += amount
                else:
                    dict_graph[giver][reciever] = amount
            if reciever not in dict_graph:
                dict_graph[reciever] = {}
        return dict_graph

    def convert_to_array_graph(self):
        # graph[i,j] indicates the amount that person i needs to pay to person j
        array_graph= np.zeros((self.n, self.n))
        for giver , reciever, amount in self.transactions:
            array_graph[self.trans_dict[giver], self.trans_dict[reciever]] = amount
        return array_graph

    def convert_dict_to_array(self, given_dict):
        converted_array= np.zeros((len(given_dict), len(given_dict)))
        for i, j in given_dict.items():
            for k, amount in j.items():
                converted_array[self.trans_dict[i], self.trans_dict[k]] = amount
        return converted_array

    def convert_array_to_dict(self, given_array):
        converted_graph= {self.reverse_trans_dict[i]:{} for i in range(len(given_array))}
        for i in range(len(given_array)):
            for j in range(len(given_array)):
                if given_array[i][j]:
                    converted_graph[self.reverse_trans_dict[i]][self.reverse_trans_dict[j]]= float(given_array[i][j])
        return converted_graph


class Delete_Cycle:
    def __init__(self, graph):
        self.graph = graph
        self.cycle = []


    def dfs_util(self, node, visited):

        if visited[node] == 1: #node is being visited, cycle detected
            self.cycle.append(node)
            return True
        
        if visited[node] == 2: #node has already been explored
            return False
        
        visited[node] = 1
        self.cycle.append(node)

        for child in self.graph[node].keys():
            if self.dfs_util(child, visited):
                return True

        self.cycle.pop()   
        visited[node] = 2 
        return False


    def detect_cycle(self):
        visited={key:0 for key in self.graph.keys()}  #0 = not visited, 1= visiting, 2= fully visited
        self.cycle = []

        for node in self.graph.keys():
            if visited[node] == 0:
                if self.dfs_util(node, visited):
                    return True
        return False


    def del_cycles(self):

        while self.detect_cycle():

            # correct the cycle list to start and end in the same node
            n= len(self.cycle)
            cycle_start = self.cycle[n-1]
            self.cycle = self.cycle[self.cycle.index(cycle_start):]

            # find the minimum transaction in the cycle
            exp= []
            for i in range(len(self.cycle)-1):
                exp.append(self.graph[self.cycle[i]][self.cycle[i+1]])
            x= min(exp)

            for j in range(len(self.cycle)-1):
                self.graph[self.cycle[j]][self.cycle[j+1]] -= x

            # delete the zero transactions
            exp= [i - x for i in exp]
            for i, ex in enumerate(exp):
                if ex == 0:
                    del self.graph[self.cycle[i]][self.cycle[i+1]]

            self.cycle = []         
    

    def answer(self):
        self.del_cycles()
        return self.graph
        
 
class Greedy_Debt_Simplification:

    def __init__(self, graph):
        self.graph = graph
        self.givers= []
        self.recievers= []
        self.n= len(self.graph)
        self.amounts= {}

    #for each user, calculate the amount he/she ows or has to pay
    def calculate_amount(self):
        gain = {node:0 for node in self.graph}
        give = {node:0 for node in self.graph}

        for u, neighbors in self.graph.items():
            for v, amount in neighbors.items():
                gain[v] += amount
                give[u] += amount

        self.amounts = {node: gain[node]-give[node] for node in self.graph}

    #construct 2 heap structures, one for the givers and one for the recievers
    def constructQ (self):
        for node , amount in self.amounts.items():
            if amount > 0:
                hq.heappush(self.recievers, (-amount, node))
            elif amount < 0:
                hq.heappush(self.givers, (amount, node))


    def simplify_debts(self):
        new_graph = {node:{} for node in self.graph}

        while self.givers and self.recievers:

            # pop the largest values for givers and recievers, and try to match them together
            giver_amount, giver_id= hq.heappop(self.givers)
            reciever_amount, reciever_id= hq.heappop(self.recievers)

            transaction_val= min(-giver_amount, -reciever_amount)

            # record the transaction made
            new_graph[giver_id][reciever_id] = transaction_val

            giver_amount += transaction_val
            reciever_amount += transaction_val

            #update the heaps
            if giver_amount < 0:
                hq.heappush(self.givers, (giver_amount, giver_id))

            if reciever_amount < 0:
                hq.heappush(self.recievers, (reciever_amount, reciever_id))

        return new_graph

    def answer(self):
        self.calculate_amount()
        self.constructQ()
        new_graph= self.simplify_debts()
        return new_graph


class Max_Flow_Simplification:
    def __init__(self, graph):
        self.graph = graph
        self.n = len(self.graph)
        self.level = [-1] * self.n
        self.parent = [-1] * self.n

        
    def find_level(self, source):
        self.level[source] = 0
        queue = [source]

        while queue:
            node = queue.pop(0)

            for neighbor in range(self.n):
                if self.level[neighbor] == -1 and self.graph[node][neighbor]:
                    self.level[neighbor] = self.level[node] + 1
                    queue.append(neighbor)

    def dfs(self, node, sink):
        if node == sink:
            return True
        for neighbor in range(self.n):
            if self.graph[node][neighbor] and self.level[neighbor] == self.level[node]+1:
                self.parent[neighbor] = node
                if self.dfs(neighbor, sink):
                    return True
        return False
                
    def max_flow(self, source, sink):
        #self.residual = self.graph.copy()
        flow = 0

        while True:
            self.level = [-1]* self.n
            self.find_level(source)
            if self.level[sink] == -1:
                break
            
            self.parent= [-1]* self.n
            if not self.dfs(source, sink):
                break

            path_flow = float('inf')
            s= sink

            while s!= source:
                path_flow = min(path_flow, self.graph[self.parent[s]][s])
                s= self.parent[s]

            s= sink
            while s!= source:
                self.graph[self.parent[s]][s] -= path_flow
                s= self.parent[s]

            flow += path_flow

        return flow
    
    def update_graph(self):
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    mf = self.max_flow(i, j)
                    if mf > 0:
                        self.graph[i][j] = mf
        return self.graph


class Linear_Programming_Simplification:
    def __init__(self, balances):
        self.balances = balances
        self.creditors = [i for i, bal in self.balances.items() if bal > 0]
        self.debtors = [i for i, bal in self.balances.items() if bal < 0]
    
    def LP(self):

        num_variables = len(self.creditors) * len(self.debtors)
        c = [1] * num_variables
        bounds = [(0, None)] * num_variables
        
        A_eq = []
        b_eq = []

        for i, debtor in enumerate(self.debtors):
            A_row = [0] * num_variables
            for j , creditor in enumerate(self.creditors):
                A_row[i * len(self.creditors) + j] = 1
            A_eq.append(A_row)
            b_eq.append(-self.balances[debtor])

        for j, creditor in enumerate(self.creditors):
            A_row = [0] * num_variables
            for i, debtor in enumerate(self.debtors):
                A_row[i * len(self.creditors) + j] = 1
            A_eq.append(A_row)
            b_eq.append(self.balances[creditor])

        res = linprog(c, A_eq = A_eq, b_eq = b_eq, bounds = bounds)
        if not res.success:
            raise ValueError('linear programming did not converg')
        
        transactions = []
        x = res.x
        for i , debtor in enumerate(self.debtors):
            for j , creditor in enumerate(self.creditors):
                amount = float (x[i * len(self.creditors) +j])
                if amount > 0:
                    transactions.append([debtor , creditor , amount])
        return transactions

    def MILP(self):  # mixed integer linear programming
        prob = LpProblem('DebtSimplification', LpMinimize)

        x = { (i, j): LpVariable(f'x_{i}_{j}', lowBound = 0) for i in self.debtors for j in self.creditors} # x[i, j] represents the amount transacted from i to j
        y = { (i, j): LpVariable(f'y_{i}_{j}', cat = 'Binary') for i in self.debtors for j in self.creditors}  #y[i, j] is a binary variable indicating if a transaction occurs between i and j

        prob += lpSum(y[i, j] for i in self.debtors for j in self.creditors)  # objective function is minimizing sum of y, the number of transactions

        for i in self.debtors:
            prob += lpSum(x[i, j] for j in self.creditors) == -self.balances[i]   # ensuring all debts are paid
        
        for j in self.creditors:
            prob += lpSum(x[i, j] for i in self.debtors) == self.balances[j]   # ensuring all credits are fulfilled

        M = sum(abs(self.balances[bal]) for bal in self.balances)

        for i in self.debtors:
            for j in self.creditors:
                prob += x[i, j] <= M * y[i, j]      # linking x , y: if x>0, then y must be 1

        prob.solve(PULP_CBC_CMD(msg=False))

        transactions = []
        for i in self.debtors:
            for j in self.creditors:
                if value(x[i, j]) > 0:
                    transactions.append([i, j, value(x[i, j])]) 
        return transactions


def num_transactions(graph):
    num = 0
    for i, j in graph.items():
        num += len(graph[i])
    return num

def construct_transactions(nodes, edges):
    transactions = []
    for i in range(edges+1):
        transactions.append([random.randint(0, nodes), random.randint(0, nodes), random.randint(1, 200)])
    return transactions


def centrality_calculation(graph, balances):
    graph = nx.DiGraph(graph)
    cen = (nx.in_degree_centrality(graph))
    sorted_cen = sorted(cen.items(), key = lambda x : x[1], reverse = True)
    high_cen_nodes = []
    for node, cent in sorted_cen:
        if cent == sorted_cen[0][1]:
            high_cen_nodes.append(node)

    center = high_cen_nodes[0]
    high_bal = -float('inf')
    for node in high_cen_nodes:
        node_bal = balances[node]
        high_bal = max(node_bal, high_bal)
    center = list(balances.keys())[list(balances.values()).index(high_bal)]
    return center
    
transactions = construct_transactions(300, 600)

def final_answer(transactions):
    Graph= Construct_graph(transactions)
    Graph.construct_transaction_dict()
    init_dict_graph = Graph.convert_to_dict_graph()
    Cycle = Delete_Cycle(init_dict_graph)
    graph_no_cycle = Cycle.answer()

    greedy= Greedy_Debt_Simplification(graph_no_cycle)
    greedy.calculate_amount()
    balances = greedy.amounts

    n_nodes = len(graph_no_cycle)
    n_edges = num_transactions(graph_no_cycle)

    # use mixed integer linear programming if the number of nodes is less than 12. it gives the optimum answer and is fast enough with samll graphs
    if n_nodes <= 12:
        milp = Linear_Programming_Simplification(balances)
        trans_milp = milp.MILP()
        New_graph = Construct_graph(trans_milp)
        final_graph = New_graph.convert_to_dict_graph()
        print('MILP used')
    
    else:
        # if the number of edges is samller than half the number of nodes (sparse graphs) max flow probably works better than greedy. 
        #for graphs larger than 500 nodes, max flow is computationaly expensive.
        if n_edges <= int((n_nodes//2)+5) and n_nodes <= 500:

            # perform max flow simplification
            dict_graph = Graph.convert_dict_to_array(graph_no_cycle)
            MF = Max_Flow_Simplification(dict_graph)
            semi_final_graph = MF.update_graph()
            semi_final_1 = Graph.convert_array_to_dict(semi_final_graph)
            semi_final_1_n_edges = num_transactions(semi_final_1)

            # perform greedy simplification
            semi_final_2 = greedy.answer()
            semi_final_2_n_edges = num_transactions(semi_final_2)

            # choose the best answer:
            if semi_final_1_n_edges < semi_final_2_n_edges:
                final_graph = semi_final_1
                print('max flow used')
            else:
                final_graph = semi_final_2
                print('greedy used')
        
        else:
            final_graph = greedy.answer()
            print('else greedy is used')

    # sometimes linear programing can give good answers
    if n_nodes < 300:
        final_n_edges = num_transactions(final_graph)
        lp = Linear_Programming_Simplification(balances)
        trans_lp = lp.LP()
        New_graph = Construct_graph(trans_lp)
        semi_final_3 = New_graph.convert_to_dict_graph()
        semi_final_3_n_edges = num_transactions(semi_final_3)
        if final_n_edges > semi_final_3_n_edges:
            final_graph = semi_final_3
            print('LP used')

    # centrality calculation
    center_node = centrality_calculation(init_dict_graph, balances)

    return final_graph, center_node



