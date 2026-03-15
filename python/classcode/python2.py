# str
# concat
# protocol = 'https:'
# domain = 'google.com'

# print(protocol + domain)  # https://google.com
# print(protocol + " " + domain)  # https:// google.com
# print(f'hello\n{protocol}')
#
# print('hello\n'*10)
# print('-'*70)

# print(f'please visit {protocol}//{domain} ({1 + 666})')

# ask the user to insert his name and last name in 2
# different rows
# i) print the first name and the last name using f''
# ii) print the firstname in capital and the last name in title
# iii) declare a new variable with the name full_name
#      that will have the value of the firstname and the
#      lastname

# hint input() , +
#
# first_name= input('please enter your firstname : ')
# last_name= input('please enter your last name : ')
#
# # i
# # print(f'{first_name} {last_name}')
#
# # ii
# print(f'{first_name.upper()} {last_name.title()}')
#
# # iii
# full_name = first_name+' '+last_name
# full_name = f'{first_name} {last_name}'

# a = 10
# b = 10.0

# print(f'{a}  {b}')
# print(f'{a} > {b} ->  {a > b}')  # False
# print(f'{a} < {b} -> {a < b}')  # False
# print(a >= b)  # True
# print(a <= b)  # True
# print(a != b)
# ==========================


# sen = 'pizza with pineapple pizza'
# ===== is , len
# print(len(sen) > 50)
# print(len(sen) == 10*2)
# print(sen[:5] == "pizza")  # True

# print('Pizza' in sen.title())  # True
# print(sen.count('pizza') > 1)  # False


# x = 10
#
# if x > 5:  # condition
#     # True block
#     print('x is greater than 10')
#     print('this is the code form the true block')
# # always
# print('print after the if statement')
#


# password = 'shawarma'
#
# if 'sh' in password:
#     print('strong password')
# else:
#     print('easy password')
# print('welcome boss')
#
#
# # אם סיסמתך מכיה sh אז אני מדפיס ססימה חזקה
# # אחרת
# # אם הסיסמה היא לא סיסמה חזרה

##########

#
# if condition :
#     true block
# else:
#     false block


password = input('enter a suggested password please : ')

if len(password) > 8 and password[0] == 'R':
    # true
    # R12345678
    print('nice password !!!!!!!!!')
else:
    print('either the password is short or you started it with another char that is not R')

print('thanks')

# nested if