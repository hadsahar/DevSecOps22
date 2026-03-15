# exercise 1 :
# ask the user to enter his id number
# check if the id number is valid
#  a valid id number contain 9 digits


# id = input('enter your id : ')  # 0236559887 -> 236559887
# if len(id) == 9 and id.isdigit():
#     print('valid id')
# else:
#     print('invalid id')

# exercise 2:
# fact: a pizza has 8 slices
# you are planning a party, and you want order pizza for your friends
# you have a math issues so you decided to build python application to calc the number of slices each one gonna have and the left-overs,
# write a python code that asks the user how many participants they invited
# and how many pizza's ordered
# the application must show the number of slices per person and the leftovers
# and if the leftovers is exactly half of the slices per person number
# print 'each one will get a 0.5 meal yaaaay'

#
# friends = int(input('please enter the number of friends :'))
# pizza = int(input('please enter the number of pizza :'))
# total_slices = pizza * 8
# slice_per_person = total_slices // friends
# # leftover = (total_slices) - slice_per_person * friends # leftovers
# leftover = total_slices % friends
# print(f'summary\n\n{pizza=}\n{total_slices=}\n{friends=}\n{slice_per_person=}\n{leftover=}')
# if leftover == slice_per_person / 2:
#     print('each one will get a 0.5 meal yaaaay')


# exercise 3 :
# ask the user to insert value from 0-2
# 0- for printing his name
# 1- for calculate his age
# 2- for printing the half of his address
#
# if the user chooses 0 then:
# ask his name , save it in a var , print the name in title
# if the user chooses 1 :
# ask for his birth-year and calc his age please
# if the user hit the 2 :
# ask for his address and print half of it

# print('''welcome
# press 0 to print your name
# press 1 to calc your age
# press 2 to print your address with a bug''')
#
# choice = input('your choice :')

# if choice == '0':
#     name = input('enter your name : ')
#     print(name.title())
#
# elif choice == '1':
#     birth_year = int(input('what is your birth year :'))
#     print(f'your age is {2026 - birth_year}')
# elif choice == '2':
#     address = input('what is address :')
#     print(address[:len(address) // 2])
# else:
#     print('invalid input')

# match choice:
#     case '0':
#         name = input('enter your name : ')
#         print(name.title())
#     case '1':
#         birth_year = int(input('what is your birth year :'))
#         print(f'your age is {2026 - birth_year}')
#     case '2':
#         address = input('what is address :')
#         print(address[:len(address) // 2])
#     case _:
#         print('invalid')


################ elif ################

# between

# 0________x____________________80

# x = 6
# # print(x<80 and x > 0)
# print(0 < x < 80)
# grade = 94

# if grade > 90:  # 91-999+
#     print('A')
# elif 90 >= grade > 80:  # 81-90
#     print('B')
# elif 80 >= grade > 70:  # 71-80
#     print('C')
# else:
#     print('F')

# if grade > 90:  # 91-999+
#     print('A')
# elif grade > 80:  # 81-90
#     print('B')
# elif grade > 70:  # 71-80
#     print('C')
# else:
#     print('F')

# short handed if

# if condition :
#     # true block
# else :
#     #false block


# exercise : write a greeting app that greet the user by his age

# age = int(input('enter you age : '))
#
# if age > 20:
#     print('hello adult')
# else:
#     print('hello child')
#
# print('hello adult' if age > 20 else 'hello child')
# true command  if condition else false command

# example : ask the user for a number
# if the number is positive print positive else print negative

# x = 8
# result = "positive" if x >=0 else 'negative'
# print(result)


# a = 10
# b = -7
#
# # in a single line of code print the max between a and b
#
# if a > b:
#     print(a)
# else:
#     print(b)
#
# print(a if a > b else b)
# # c#,java ,javascript print(a ? a > b: b)

#


# sites = ['google.com', 'youtube.com', 'facebook.com']
#
# print(sites)
# print(sites[0])
# print(sites[:2])
#
# sites.append('x.com')
# print(sites)
#
# sites.remove('google.com')  # delete by value
# print(sites)
# sites.pop(0)
# del sites[1]
# print(sites)

# print(sites.count('google'))
# print(sites[0].count('google'))
# print(sites.index('facebook.com'))  # 2
# print(sites.index('instagram.com'))  # instagram is not in list
#
# sites.clear()
# print(sites)


# grades = [97, 88, 14, 99, 100, 8, 45, 54]
#
# print(grades)
# # grades.sort()  # A-Z 0-9
# grades.reverse()
# # grades.sort(reverse=True)
# print(grades)

# +++++++++++++++++++++++++++++++  tuple ++++++++++++++++++++++++

# passwords = ('pizza4life', 'hodi', 123456)
#
# print(type(passwords))
#
# print(passwords[0])
# passwords[1] = 'aviel' # Error


############ set ########


menu = {'kebab', 'shawrma', 'kebab', 1, 5, 2, 2, 2, 2, 2, True, False, 0}
print(menu)
menu.add(2)
menu.add(88)
print(menu)
