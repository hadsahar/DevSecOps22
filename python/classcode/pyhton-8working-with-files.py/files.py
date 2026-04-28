# print('files in python')
# # ab path /Users/hothaifa/workspace/DevSecOps-22/python/classcode/pyhton-8working-with-files.py/my-file.txt
# file = open('./my-file.txt','r') # var fileIOWrapper

# # print(file) # <_io.TextIOWrapper name='./my-file.txt' mode='r' encoding='UTF-8'>

# # print(file.readable()) # is this file open for reading ?
# # print(file.writable())  # is this file open for writing ?

# # cursor = file.tell()
# # print(f'cursor -> {cursor}')

# # file.seek(cursor+3)
# # cursor = file.tell()
# # print(f'cursor -> {cursor}')

# # print(file.read(10))
# # print(file.tell())
# # file.seek(0)
# # print(file.read(20))


# # l1 = file.readline()
# # print(l1)
# # l2 = file.readline()
# # print(l2)

# # p = file.readlines()
# # # print(p)
# # # print(p)
# # for line in p :
# #     if 'google.com' in line:
# #         # print(line.upper()[-1:])  # /n
# #         print(line.upper()[:-1])  # ....... X/n
# #         break


# file.close()

# # print(file.writable()) ## ValueError: I/O operation on closed file



# file = open('my-file.txt','r+')
# file.close()
# print('end of file')

# with open('my-file.txt','a+') as f:
#     # print(f.readlines())
#     if f.writable():
#         f.seek(0)
#         print(f.tell())
#         f.writelines(['hello','my'])
# print('end of file')



# execise 1
# with open('my-file.txt','r+') as file:
#     lines = file.readlines() # list 
#     print(file.tell())
#     file.seek(0)
#     print(lines)
#     file.write('rotem\n')
#     file.writelines(lines) # LIST -> item - line



# with open('names.txt','w+') as log:
#     print(log.read())
    

