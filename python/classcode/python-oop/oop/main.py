class Cat():
    # data
    def __init__(self,name , color ,age ,weight=2.7):
        self.name =name
        self.color=color
        self.age=age
        self.weight = weight + 1
    
    def __str__(self):
        return f'cat obj {self.name} {self.age} {self.color} {self.weight}'
    

c1= Cat('betsiii','black',12,3)

print(c1)
# print(c1.name)
# print(c1.weight)
x = str(c1)
print(x)


