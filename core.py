import numpy as np
import heapq as hq
transactions= [['a', 'b', 50], ['b', 'c', 30], ['c', 'a', 20], ['d', 'a', 10]]
transactions_2= [['a','b',1000], ['a','c',2000], ['b','c',5000]]
transactions_3= [[0,0,2], [0,1,63], [0,3,85], [0,4,49], [1,1,76], [1,4,27], [2,3,17], [3,0,73], [3,1,32], [3,2,50], [3,3,6], [3,4,71], [4,1,86], [4,4,10]] 

def convert_to_graph(transactions):
    transaction_dict= {}
    for giver, reciever, a in transactions:
        if giver not in transaction_dict.keys():
            transaction_dict[giver]= len(transaction_dict)
        if reciever not in transaction_dict.keys():
            transaction_dict[reciever]= len(transaction_dict)

    n= len(transaction_dict)
    # graph[i,j] indicates the amount that person i needs to pay to person j
    graph= np.zeros((n, n))
    for giver , reciever, amount in transactions:
        graph[transaction_dict[giver], transaction_dict[reciever]] = amount

    return transaction_dict, graph

transaction_dict, graph= convert_to_graph(transactions_3)
reverse_dict= {i:j for j, i in transaction_dict.items()}

print(graph)

class greedy_debt_simplification:

    def __init__(self):
        self.givers= []
        self.recievers= []
        self.n= len(graph)
        self.amounts= [0 for _ in range(self.n)]

    #for each user, calculate the amount he/she ows or has to pay
    def calculate_amount(self, graph):
        for i in range(self.n):
            gain= np.sum(graph[:, i])
            give= np.sum(graph[i, :], axis=0)
            self.amounts[i]= int(gain- give)

    #construct 2 heap structures, one for the givers and one for the recievers
    def constructQ (self):
        for i , amount in enumerate(self.amounts):
            if amount > 0:
                hq.heappush(self.recievers, (-amount, i))
            elif amount < 0:
                hq.heappush(self.givers, (amount, i))

    def simplify_debts(self):
        answer= []
        while self.givers and self.recievers:

            # pop the largest values for givers and recievers, and try to match them together
            giver_amount, giver_id= hq.heappop(self.givers)
            reciever_amount, reciever_id= hq.heappop(self.recievers)

            transaction_val= min(-giver_amount, -reciever_amount)

            # record the transaction made
            answer.append([reverse_dict[giver_id], reverse_dict[reciever_id], transaction_val])

            giver_amount += transaction_val
            reciever_amount += transaction_val

            #update the heaps
            if giver_amount < 0:
                hq.heappush(self.givers, (giver_amount, giver_id))

            if reciever_amount < 0:
                hq.heappush(self.recievers, (reciever_amount, reciever_id))

        return answer

    def answer(self):
        self.calculate_amount(graph)
        self.constructQ()
        answer= self.simplify_debts()
        print(self.amounts)
        print(answer)



        
s=greedy_debt_simplification()
s.answer()


