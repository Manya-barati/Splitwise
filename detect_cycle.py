import heapq as hq
import numpy as np

transactions_1= [[0,0,2], [0,1,63], [0,3,85], [0,4,49], [1,1,76], [1,4,27], [2,3,17], [3,0,73], [3,1,32], [3,2,50], [3,3,6], [3,4,71], [4,1,86], [4,4,10]] 
transactions_2 = [['A', 'B', 500], ['B', 'C', 300], ['C', 'D', 200], ['C', 'A', 50], ['D', 'A', 100], ['E', 'F', 400], ['F', 'E', 300]]
transactions_3 = [[0, 1, 10], [0, 2, 20], [1, 2, 5], [1, 3, 10], [2, 3, 15]]
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

Graph= Construct_graph(transactions_6)
Graph.construct_transaction_dict()
print(Graph.trans_dict)
graph_1 = Graph.convert_to_dict_graph()
print('initial graph', graph_1, '\n')

Cycle = Delete_Cycle(graph_1)
graph_2 = Cycle.answer()
print('graph with no cycle', graph_2, '\n')

graph_2_converted = Graph.convert_dict_to_array(graph_2)
MF = Max_Flow_Simplification(graph_2_converted)
graph_3= MF.update_graph()
graph_3_converted = Graph.convert_array_to_dict(graph_3)
print('after max flow simplification', graph_3_converted, '\n')

greedy= Greedy_Debt_Simplification(graph_2)
graph_4 = greedy.answer()
print('after greedy simplification', graph_4)