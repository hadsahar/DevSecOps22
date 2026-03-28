# dict
# guy_grade = 50
# dylan_grade = 80
# eitan_grade = 90
# rotem_grade = 100
#
# grades_list = [50, 80, 90, 100]
# print(f'rotem grade is : {grades_list[3]}')
#
## lets have it with dict
# grades = {'guy': 50, 'dylan': 80, 'eitan': 90, 'rotem': 100}
# print(type(grades))
# print(grades)  #{'guy': 50, 'dylan': 80, 'eitan': 90, 'rotem': 100}
# print(grades['guy'])  # 50
# print(grades['rotem'])  # 100
# print(grades['hen']) # x error

# print(grades.keys())  # list of the key
# print(type(grades.keys()))
# print(grades.values())  # list of the values
# grades['hen'] = 99  # declare and assign value
# print(grades)
# grades['guy'] = 100  # override
# print(grades)
# del grades["guy"]  # delete item
# print(grades)

# x = grades.pop('guy')  # delete
# print(x)
# print(grades)
# grades.clear() # delete all items


# # print(grades.items())
# for item in grades.items():
#     # print(item)
#     # print(type(item))
#     if item[0] == 'rotem':
#         continue
#     print(item[1])

# for key in grades.keys():
#     print(f'grades["{key}"]')
#     print(f'the key is {key} and the value {grades[key]}')

# keys = list(grades.keys())
# values = list(grades.values())
# for index in range(len(grades.keys())):
#     print(f'key is : {keys[index]} value is : {values[index]}')

# print(list(grades.items()))
# for key, value in grades.items():  # [('guy', 50), ('dylan', 80), ('eitan', 90), ('rotem', 100)]
#     print(f'the key is {key} and the value is {value}')
#
# for k,v in grades.items():
#     print(f'{k} ->> {v}')


# exercise:

# for each dict you will find an ec2 data
# id, status, type, os,
# declare alist of dict and run
# build a health monitor that runs every 10 sec and checks the status of each one of the ec2
# take the same code and make it run on 19:40 min
import time
import datetime

# [{"name":'ec2-1'},{"name":'ec2-2'}]
# infrastructure = [
#     {'id': 'i-01', 'status': "running", 'type': 't2.micro', 'os': 'amazon linux'},
#     {'id': 'i-02', 'status': "running", 'type': 'm5.large', 'os': 'amazon linux'},
#     {'id': 'i-03', 'status': "running", 'type': 'r6.large', 'os': 'ubuntu'},
#     {'id': 'i-04', 'status': "running", 'type': 't3.micro', 'os': 'kali'}
# ]
# print(type(infrastructure))  # list
# print(type(infrastructure[0]))  # dict
# print(type(infrastructure[0]['status']))  # str  infrastructure -> 0 -> status

# {key : value}
# 'str' : 'str'


# while True:
#     date = datetime.datetime.now()
#     hours = date.hour
#     min = date.minute
#     # print(min,hours)
#     if min == 42 and hours == 19:
#         print('------- now we are going to monitor the infrastructure --------')
#         for instance in infrastructure:
#             if instance['status'] == 'running':
#                 print(f'{instance["id"]} is up and running')
#     time.sleep(60)
import random

# Write a Python script to print a dictionary where the keys are numbers that
# you can randomly set or from the user prompt
# between 1 and 15 (both included) and the values are the square of the keys.
# the dict must contain 10 items at least

# example = {5: 25, 10: 100}

# key = int
# i) random keys between 1- 15
# ii) ask the user for the number 1-15
# dict1 = {}
# iterations = 0
# while True:
#     r = input('enter a number (1-15) : (q to exit) ')
#     if r == 'q' or 15 < int(r) < 1:
#         if len(dict1) > 10:
#             break
#         else:
#             print(f'you gave {10 - len(dict1)} items to insert ')
#             continue
#     r = random.randrange(1, 15) if r == '' else int(r)
#     dict1[r] = r ** 2  # r*r
#     iterations += 1
# print(dict1)
# print(f'it tooks me {iterations} iterations to complete the job ')

# write a python code to merge to dict
# in case of conflict take the new value from the dict2
# for example :
global_tags = {'env': 'e2e', 'owner': 'all', 'project': 'AIdev'}
s3_tags = {'env': 'e2e', 'owner': 'devops', 'parent_asset_id': '46128461'}

# merged_tag = {'env': 'e2e', 'owner': 'devops', 'project': 'AIdev', 'parent_asset_id': '46128461'}
#              {'env': 'e2e', 'owner': 'devops', 'project': 'AIdev', 'parent_asset_id': '46128461'}

# merged_tags = {}
# # copy global tags
# for key in global_tags:
#     merged_tags[key] = global_tags[key]
# # override / add from s3 tags
# for key in s3_tags:
#     merged_tags[key] = s3_tags[key]

# merged_tags = global_tags.copy()
# merged_tags.update(s3_tags)

# merged_tags = global_tags | s3_tags

# print(merged_tags)

# write a python code to sum all the values
cpu_usage = {
    'service_auth': 129,
    'service_validate': 60,
    'service_payment': 122
}

# sum = 0
# for key in cpu_usage:
#     sum += cpu_usage[key]
#
# print(sum)

sum = sum(list(cpu_usage.values()))
print(sum)