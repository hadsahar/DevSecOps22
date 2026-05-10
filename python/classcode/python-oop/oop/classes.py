from abc import ABC,abstractmethod

class Accoount(ABC):
    @abstractmethod
    def transfer(self):
        pass

    def __init__(self,owner,id,balance):
        self.owner = owner
        self.id = id
        self.balance = balance
    
    def __add__(self,other):
        if isinstance(other,Accoount):
            return Accoount(self.owner,self.id+1 , self.balance + other.balance)
        else :
            self.balance += other
        return self
    
    def __gt__(self,other):
        return self.balance > other.balance
    
    def __lt__(self,other):
        return not self > other
    
    def __str__(self):
        return f'this account belongs to {self.owner} balance is {self.balance}'
    

class CheckingAccount(Accoount):
    def __init__(self,owner,id,balance,credit_limit,credit_score):
        super().__init__(owner,id,balance)
        # Accoount.__init__(self,owner,id,balance)
        self.credit_score= credit_score
        self.credit_limit= credit_limit
    def transfer(self):
        print('transfering . . .')

    
checking_Accoun1= CheckingAccount('aviel',123,10000,2000,950)

print(checking_Accoun1.owner)

# acc =Accoount('moshe',2,3223)

# print(acc)

