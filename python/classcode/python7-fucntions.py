# # keys = ["env", "owner", "project"]
# # values = ["prod", "devops", "payments"]
#
# # result = {}
# #
# # if len(keys) == len(values):
# #     for i in range(len(keys)):
# #         result[keys[i]] = values[i]
# #
# #
# # for k,v in result.items():
# #     print(f'{k} => {v}')
# #
#
# # short-handed for
# # list comprehension
#
#
# # for i in range(len(keys)):
# #         result[keys[i]] = values[i]
#
# results = {keys[i]: values[i] for i in range(len(keys))}
# print(results)
#
#
# ##
#
# # given a this list [1,23,31245,235,2365,346,45,756,8,679,678,9078,1221]
# #  create to 2 lists 1 with all the odd numbers
# # the second contains the numbers above the avg of the list itself
# l1 = [1, 23, 31245, 235, 2365, 346, 45, 756, 8, 679, 678, 9078, 1221]
#
# # odds = []
# # for number in l1:
# #     if number % 2 == 0:
# #         odds.append(number)
# #
# # print(odds)
#
# odds = [x for x in l1 if x % 2 ]
# print(odds)
#
# # avg = max(l1) / len(l1)
# # print('avg', avg)
# # above_avg = [x for x in l1 if x > avg]
# # print(above_avg)
# #
# salaries = [10000, 200000, 10000, 1058641, 5604, 81, 89564, 8651, 564, 1655, 5861, 654, 68541, 4987, 4986, 1685, 74986,
#             4086]
# tax = 0.23
# #
# net_salaries = [x*(1-tax) for x in salaries if x >= 10000]
# #
# # print(salaries)
# # print(net_salaries)


################ functions ################

# a function is a reusable clock of code that can performs a task


# def function_name():
#     print('hello')
#
#
# function_name()
# function_name()

#
# def greet():  # input X outputX
#     '''
#     this function print hello to the user
#     :return:
#     '''
#     print('hello')
#
#
# def greet_with_name(name):  # input V output X
#     print(f'hello {name}')  # greet_with_name.name
#
#
# def greet_with_name_and_age(name: str, age: int):
#     print(f'hello {name} , {age} years old ')
#
#
# def greet_all(names: list):
#     for name in names:
#         greet_with_name(name)
#
#
# greet()
# greet_with_name('hodi')  # main.name
# greet_with_name_and_age('guy', 50)
#
# greet_all( ['or', 'elia', 'rotem'] )
# # greet_all(150) # error


# def your_sum():
#     x = 12 + 3  # x -> 15
#
#
# def my_sum(a, b):
#     return a + b
#
#
# def get_number():
#     return 66


# print(your_sum())  # -> None == null == void
# print(my_sum(1, 2))
# ans = get_number()
# print(ans)
# print(get_number())


# def login(username='spooky33'):
#     print(f'welcome back {username}')
#
#
# login()
# login('iusecahtgpt')

# def hard_login(username, password, otp=11, token=1):
#     pass
#
#
# print()
# hard_login(1, 2, 3, 4)
# # hard_login(username=123, otp=1, 44, password=1) # X Error
# hard_login(14, 55, token=88)
#

# you need to add code to the git using python function
# this function checks some parameters before adding and pushing the changes
# params = userid , ticket_number , version , approved , env
# the code is not approved by default and the env can be dev or prd and version 0.1
# if the ticket number starts with infraXXXXX  and the userid contains exactly 6 digits
# ask for approval if the approval submitted push the code
# import time
#
#
# def git_save(userid, ticket_number, version=0.1, approved=False, env='dev'):
#     if approved:
#         print(f'{userid} saved the code .....')
#         time.sleep(2)
#         print(f'git add ..........{1 + version}')
#         time.sleep(1)
#         print(f'git commit -m {ticket_number} fix ..')
#     else:
#         inline_approval = True if input('approved ? Y/N only ') == 'Y' else False
#         if inline_approval:
#             print(f'{userid} saved the code .....')
#             time.sleep(2)
#             print(f'git add ........{version}')
#             time.sleep(1)
#             print(f'git commit -m {ticket_number} fix ..')
#         else:
#             print('declined ')
#             exit()
#
#
# git_save(147852, 'infra123')  # userid, ticket_number, version=0.1, approved=False, env='dev'
# git_save(147852, ticket_number='infra123', env='prd')  # userid, ticket_number, version=0.1, approved=False, env='dev'
# # git_save(userid=147852, env='prd', 'infra123') #X Error  # userid, ticket_number, version=0.1, approved=False, env='dev'
# git_save(147852, 'infra123',1.1,True,'dev')
# git_save(userid=147852,version=0.5,approved=True,ticket_number='infra123',env='prd')

################ *args,**kwargs #################

# def total(a, b):
#     return a + b
#
#
# def total(a, b, c):
#     return a + b + c
#
#
# def total(a, b, c, d, e, f):
#     return a + b + c + d + e + f
# not a python practice

# override
# overload


# def total(*args):  # xargs
#     print(type(args))
#     sum = 0
#     for arg in args:
#         sum += arg
#     return sum
#
#
# print(total(1, 2, 3, 4, 5))
# print(total(1))
# print(total(55, 77))
# print(total('a','b','c',1,2,3)) # X bad


# def foo(a, *args, z=123):
#     print(a)
#     print(args)
#     print(z)


# foo(5)  # a= 5  args= ()  z=123
# foo(1, 2, 3, 4, 5, 6, 7, 8, 9)  # a = 1 args =(2,3,4,5,6,7,8,9) z =123
# foo(1, 1, 2, 22, 3, 3)  # a = 1 args= (1,2,22,3,3) z=123
# foo(88, 84, 4, 4, 8, 48, 64, 6, z=88)
# foo((8, 1, 2, 3, 4, 5, 8),123,123,12312,3213) # a = (8, 1, 2, 3, 4, 5, 8)


# def print_the_names(count, *names, lines=1):  # *args
#     print(type(names))
#     for name in names:
#         for i in range(lines):
#             print()
#         print(name.upper())
#
#
# # print_the_names('elad', 'sahar')  # 2
# # print_the_names()  # 0
# print_the_names(4, 'avi', 'moshe', 'ziv', 'mor', 'eden', 'yaki')


# print('hodi', 'wallaak', 'hamburger',sep='@gmail.com ' , end='shoooshi')
# print()
#
# exit()

# import random
#
# random.randrange()
#
# len()


# def objs(**kwargs):  # dict
#     dict1 = {}
#     print(type(kwargs))
#     for k, v in kwargs.items():
#         dict1[k] = kwargs[k]
#         if k == 'clr':
#             dict1['color'] == dict1['clr']
#
#
# # fname first name namee name1
#
#
# objs(len=11, size='3XL', color=144)
# objs(len=11, size='3XL', clr=144)
#
# objs(cal=1990, toppings='cheese')


# we have a 2 end users that allowed to create a cars object
# each car object {dict} saved in the database as the following
# color , model , make , year
# problem :
# each on of the users write the keys in his way :
# color attribute :  can be clr cr c or color
# make attribute : can be one of those make m mk manufacturer
# year
# model can be int or str

# write me a function that can work with the 2 endusers
# and return the dict to the user please


# def car_def(model, year, **kwargs):
#     car = dict()
#     car['model'] = model
#     car['year'] = year
#     for k, v in kwargs.items():
#         if k in ['clr', 'cr', 'c', 'color']:
#             car['color'] = v
#         elif k in ['make', 'm', 'mk', 'manufacturer']:
#             car['make'] = v
#     return car
#
#
# car1 = car_def('m4', 2026, make='bmw', c='black')
# car2 = car_def('Q7', 2020, manufacturer='audi', clr='white')
#
#
# print(car1)
# print(car2)