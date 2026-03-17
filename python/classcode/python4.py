# ask the user for 3 names and add them to a list

# names = []
#
# names.append(input('enter a name : '))
# names.append(input('enter a name : '))
# names.append(input('enter a name : '))
#
# print(names)

# ask the user for 3 meals print only the unique meals

# meals = set()  # without duplication
#
# meals.add(input('enter a name : '))
# meals.add(input('enter a name : '))
# meals.add(input('enter a name : '))
#
# print(meals)

#


# l1 = [1, 2, 3, 4, 4, 4, 5, 6, 7, 8, 9]
# casting s1 = set(l1)
# i- print the list without duplications
# ii- print half of this list
# iii- find the first index of 4 and the last index of 4
# iv - add the first and the last items and divide by the len
# v - print the list backward  9 8 7 6 5 4 4 4 ...

# print(l1)
# s1 = set(l1)  # list -> set
# print(f'i- {s1}')
# print(f'ii- {l1[:len(l1) // 2]}')
# print(f'iii - {l1.index(4)},{l1.index(4,l1.index(4)+2)}')
# print(f'iv - { (l1[0] + l1[-1]) /len(l1)}')
# l1.reverse()
# print(f'v - { l1 }')


# for loop

# name = 'sahar'
#
# for c in name :
#     print(c)

# sen = 'joey doesnt share food'
#
# print(sen.count('e'))
# counter = 0
# for ch in sen:
#     if ch == 'e':
#         counter = counter + 1
# print(counter)

# cars = ['audi', 'bmw','tesla','mazda']
# # print all the cars and the first char of each item
# for i in cars:
#     print(f'{i} {i[0]}')


# salaries = [20_000, 10_000, 1500, 5400, 3200]
# tax = 0.18
#
# # print all the salaries after tax reduction
# # create a new list and add the neto salaries to it
# net_salaries = []
#
# for salary in salaries:
#     salary *= (1 - tax)  # salary = salary * (1-tax)
#     net_salaries.append(int(salary))
# print(salaries)
# print(net_salaries)

grades = [100, 50, 20, 60, 50, 80, 80, 90, 100]

# what is the max grade
# what is the min grade
# print the sum of all items
# print the avg
#
# print(max(grades))
# print(min(grades))
#
# my_max = grades[0]
# my_min = grades[0]
# for grade in grades[1:]:
#     if grade > my_max:
#         my_max = grade
#     if grade < my_min:
#         my_min = grade
#
#
# print(f'max = {my_max}')
# print(f'min = {my_min}')


print(sum(grades))
my_sum = 0
for grade in grades:
    my_sum += grade
print(my_sum)
print(my_sum / len(grades))
