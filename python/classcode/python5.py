
import datetime
# name = '___'
# #         ^
# for i in name :
#     print('hello maaa nishmaa')
#
# # _
# # _
# # _

# range(10) -> [\0,1,2,3,4,5,6,7,8,9/]
# print(list(range(10)))
# print(list(range(94)))
# print(list(range(5,100)))
# print(list(range(1,10,2)))
# print(list(range(0,11,2)))
# range(n) from 0 to n-1
# range(n,m) from n to m-1
# range(n,m,z) from n to m-1 in z steps
#
# print(list(range(3, 0, -1)))
#
# for i in range(3, 0, -1):  # [3,2,1]
#     # print(i)
#     print(f'enter your password you have { i } tries left ')
#     guess = input()
#     if guess == 'hjaioskbgpasi':
#         print('welcome')
#
# # print all the number that can divide by 7 without leftovers on the range 10 - 1000
# for i in range(10, 1001):
#     if i % 7 == 0:
#         print(i)
#
# # print(list(range(14,1001,7)))

# # print a list of numbers between 50 - 500 each in one line ,50 51 52 53
# for i in range(50, 501):
#     print(i)
#
# # print(list(range(50, 501))) X
#
# # print all the numbers between 500 - 50 in dec order , 500 499 498
# for i in range(500,49,-1):
#     print(i)

# for _ in range(100):
#     print('hello')

# print the next pattern
# *
# * *
# * * *
# * * * *

# for r in range(4):
#     for c in range(4):
#         if c <= r:
#             print('* ',end='')
#     print()

# for i in range(1, 5):
#     print('* ' * i)
# index       0      1       2     3        4       5
# services = ['ec2', 'ebs', 'rds', 's3', 'dynamodb', 'sqs']
# up = [True, True, True, True, False, True]

# iterate over the services and check if the services is up
# use indexes to map between the status and the svc name
# if one of the services failed stop the checking logic

# for i in range(len(services)):  # (0,1,2,3,4,5)
#     if services[i] == 's3':
#         continue
#     if up[i]:
#         print(services[i], ' is up and running')
#     else:
#         print(services[i], 'isnt working')
#         break
# print('thanks')

# if condition :
#     code
# else:
#     code
#

# code(true if condition else false)


# for i in range(len(services)):  # (0,1,2,3,4,5)
#     if services[i] == 's3':
#         continue
#     print(services[i], ' is up and running' if up[i] else services[i], 'isnt working')
#
# print('thanks')

# lives = 4
# enemies = ["vegeta", 'krillin', 'friezass', 'majin boo']
#
# for enemy in enemies:
#     print(f'goku fights {enemy}')
#
#     if enemy == 'frieza':
#         print('this fight is too dangerous | STOP!!')
#         lives = 0
#         break
#     if len(enemy) == 7:
#         print('too easy ')
#         continue
#     lives -= 1
#
# print(lives)

# meals = ['starter', 'salad', 'main dish', 'desert', 'drinks']
#
# for meal in meals:
#     if meal == 'salad':
#         continue
#     print(f'{meal} is arriving ')
#     # if meal == 'main dish':
#     #     print('No plates left :( ')
#     #     break
# else:
#     print('discount 30% for ordering all the menu')

# CICD
# steps = ["plan", "code", 'build', 'test', 'scan', 'deploy']

# in this system after apassed pipeline cicd we notify the manager that a new version is up

# for step in steps:
#     status = input(f'what is the status of the {step}')
#     if status == "passed":
#         print(f'{step} passed')
#     elif status == 'running':
#         for i in range(3):
#             status = input('Done ?? (y/n)')
#     else:
#         break
# else:
#     print('notify the manager for new version')

# services = ['ngix', 'appache storm', 'redis', 'postgres', 'api']
#
# off = None
# for service in services:
#     print(f'checking {service} ...')
#     if service == off:
#         print(f'{service} is offline XXXXXX')
#         break
#
# else:
#     print('the system is up and ready for connections ')

# pin = '1744'
# guess = input('enter the pin code : ')
# while guess != pin:
#     guess = input('enter the pin code : ')
#
# print('welcome')

# age = 15
# legal_age = 18
# while legal_age <= 18:
#     age = input('enter new age ')
#     print('hello ')

# do while
# while True:
#     x = int(input('enter a number  '))
#     if x == 100:
#         break

# ask the user for a his id number
# if the id number isnt 9 digits ask for it again
# do it 3 times only


# for i in range(3):
#     id = input('enter your id number : ')
#     if len(id) == 9:
#         print('we got the id')
#         break
# else:
#     print('try again next time')
#
# print('thank you')

# counter = 0
# id = '0'
# while counter < 3 and len(id) != 9:
#     id = input('enter your id number : ')
#     counter += 1

# i = 0
# while i < 3:
#     id_num = input('enter your id number : ')
#     if len(id_num) == 9:
#         print('we got the id')
#         break
#     i += 1


# calculater

# DRY

# do while
# while True:
#     print('press 1 for + or q to exit ')
#     print('press 2 for - or q to exit ')
#     print('press 3 for * or q to exit ')
#     print('press 4 for // or q to exit ')
#     choice = input(' : ')
#     if choice == 'q':
#         break
#     if choice in '1234':
#         x = int(input('enter a number '))
#         y = int(input('enter a number '))
#     match choice:
#         case '1':
#             print(f'{x} + {y} = {x + y}')
#         case '2':
#             print(f'{x} - {y} = {x - y}')
#         case '3':
#             print(f'{x} * {y} = {x * y}')
#         case '4':
#             print(f'{x} // {y} = {x // y}')
#         case _:
#             print('read the lines you idiot ')

# while
start_time= datetime.datetime.now()
print('press 1 for + or q to exit ')
print('press 2 for - or q to exit ')
print('press 3 for * or q to exit ')
print('press 4 for // or q to exit ')
choice = input(' : ')
while choice != 'q':
    match choice:
        case '1':
            x = int(input('enter a number '))
            y = int(input('enter a number '))
            print(f'{x} + {y} = {x + y}')
        case '2':
            x = int(input('enter a number '))
            y = int(input('enter a number '))
            print(f'{x} - {y} = {x - y}')
        case '3':
            x = int(input('enter a number '))
            y = int(input('enter a number '))
            print(f'{x} * {y} = {x * y}')
        case '4':
            x = int(input('enter a number '))
            y = int(input('enter a number '))# ========== time ========

            print(f'{x} // {y} = {x // y}')
        case _:
            print('read the lines you idiot ')
    print('press 1 for + or q to exit ')
    print('press 2 for - or q to exit ')
    print('press 3 for * or q to exit ')
    print('press 4 for // or q to exit ')
    choice = input(' : ')

end_time = datetime.datetime.now()

print(f'starts at {start_time}\nends at {end_time}')
t = end_time-start_time
print(t)



#======== imports =========

import random
import time
import datetime

# ========= random =======

# random_int = random.randint(-100, 1500)
# print(x)
#
# random_float = random.random()  # 0.0 1.0
# print(random_float)

# random_float_range = random.uniform(10.0,100.5)
# print(random_float_range)

# colors = ['red', 'blue', 'yellow', 'black']
# theme_color = random.choice(colors)
# theme_color1 = random.choice(['heads', 'tails'])
# print(theme_color)
# print(theme_color1)
#
# cards = ['Ace','king','queen', 'jack','10']
# random.shuffle(cards)
#
# print(cards)
#
# print(random.randrange(1,100,2))


# ========== time ========

# print('x')
# time.sleep(3) #in seconds
# print('y')
#
# print(time.time()) # timestamp
# print(time.ctime())

# ========== datetime ========

t = datetime.datetime.now()
print(t)
print(t.date())
print(t.time())
print(t.month)
print(t.second)
print(t.microsecond)


