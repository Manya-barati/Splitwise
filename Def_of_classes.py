class Friend():
    def __init__(self, name):
        self.name = name
        self.money = 0


class Expenses():
    def __init__(self, value, payer, owers, shares):
        self.value = value
        self.payer = payer
        self.owers = owers
        self.shares = shares


class Group():
    def __init__(self,name, type):
        self.expenses = []
        self.friends = []
        self.name=name
        self.type=type

    def add_friend(self, new_friend):
        self.friends.append(new_friend)

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.update_pay(expense)

    def update_pay(self, expense):
        total_shares = sum(expense.shares)
        amount_for_one = [expense.value * expense.shares[i] / total_shares for i in range(len(expense.owers))]
        for person in expense.owers:
            if person != expense.payer:
                self.friends[person].money -= amount_for_one[person]
                self.friends[expense.payer].money += amount_for_one[person]
