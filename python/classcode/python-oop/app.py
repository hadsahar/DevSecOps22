
# class Dog():
#     #Data
#     name='vvv'
#     age=0
#     fav_food=''
#     breed=[]
#     # funct
#     def bark(self):
#         if self.age > 0 :
#             print('whooph wooph')
#         else:
#             print('how how')
    


# d1 = Dog() # d1 is instance of DOG
# d2 = Dog() # d2 object 
# d3 = Dog() # etzem 


# print(d1) #<__main__.Dog object at 0x102721bd0>
# print(d2) #<__main__.Dog object at 0x102721c10>
# print(d3) #<__main__.Dog object at 0x102721c50>

# print(type(d1))
# print(isinstance(d1,Dog)) # true
# print(isinstance(2,Dog)) # false
# print(isinstance(2,int)) # true

# -------attribute access-----
# print(d1.name)
# d1.name='rexy'
# print(d1.name)
# print(d2.name)

# d1.last_name=33
# print(d1.last_name)

# del d1.age
# print(d1.age)

# # ------ default attribute access -----

# print(d3.__hash__())


# x='123'

# x.upper() #method
# # upper() # x

# len() # function 
# open() # function 
# print() # function 

# ------------function--------

d1.bark()
d1.age = 6
d1.bark()