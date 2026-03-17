# 1 
# casting : datatype A -> datatype b
# int() , float()

# 1.5 
# checks if elemnts inside another elemnt

# 2 else - elif 
# in else we write the false block code 
# elif helps us to create another codition if ther prev didnt metup

# 3 indent - spaces - tabs
#     code
#     code
#    code 

# # 4 
# x = float(input('please enter a number : '))
# y = float(input('please enter a number : '))

# if x > y :
#     print(x)
# else :
#     print(y)
# # short handed if 
# print(x if x >y else y )

# 5

# a=int(input('enter a number'))
# b=int(input('enter a number'))
# c=int(input('enter a number'))

# # if a >b and a > c :
# #     print(a)
# # else:
# #     if b>c and b>a :
# #         print(b)
# #     else: 
# #         if c > a and c > b:
# #             print(c)

# if c < a > b :  
#     print(a)
# elif b>c :
#         print(b)
# else: 
#     print(c)


# 6
# odd - 1,3,5,7  
# even - 0,2,4,6,8,100

# number = int(input('please enter a number: '))
# # # 4%2 =0 17%2 =1 

# # if number % 2 == 0:
# #     print('even')
# # else:
# #     print('odd')

# print(int(False))

# if number % 2:
#     print('odd')
# else:
#     print('even')

# 7
# score = 83

# if score >= 90:
#     print("A")
# elif score >= 80:
#     print("B")
# elif score >= 70:
#     print("C")
# elif score >= 60:
#     print("D")
# else:
#     print("F")


# 8
# Program: login simulation
# Hardcode: username = "admin", password = "P@ssw0rd"
# Ask the user for username and password
# Print Welcome if both correct,
# Wrong username if username wrong, Wrong password if username correct but password wrong

# username = 'admin'
# password = 'P@ssw0rd'

# username_input = input('username : ')
# password_input = input('password : ')

# if username == username_input:
#     if password == password_input:
#         print('welcome')
#     else:
#         print('password incorrect')
#     print('username is valid')
# else:
#     print('username invalid !!!!')

# # DRY - dont repeat yourself
# # nested if


# 9

# country = input('which country are you from : ')
# amount = float(input('total order amount : '))

# if amount >= 300 :
#     print('yaaaay free shipping ')
# elif country == 'IL':
#     print('shipping cost 20 ils')
# elif country == 'US':
#     print('shipping 50 ils')
# else:
#     print('shipping 70')

#10 

password = input('password required : ')
half = len(password)//2
if len(password) > 7 and password[:half] == password[half:]:
    print('valid one ')
else:
    print('incorrect password ')

