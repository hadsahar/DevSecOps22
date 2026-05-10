
class Wallet:
    def __init__(self,balance,coins,id):
        self._balance=balance # private
        self.coins=coins
        self.id=id
    def get_balance(self):
        return self._balance*0.82
    def set_balance(self,amount):
        self._balance += 0 if amount <0 else amount
        self.__apply_intrest()

    def __apply_intrest(self):
        self.__balance -= 10

class AdvWallet(Wallet):
    def __init__(self, balance, coins, id,comments):
        super().__init__(balance, coins, id)  
        self.comments =comments
    def calc_upcoming_investment(self):
        print(self._balance*10)
        

w1 = Wallet(10000,'dodgecoin',123)


# print(w1.balance)
# print(w1.__balance)
print(w1.get_balance())

aw1 = AdvWallet(10000,'dodgecoin',123,'')
aw1.calc_upcoming_investment()