import os


path = os.getcwd() # pwd cwd -> .
print(f'{path}')

command = os.system('ping -c 3 google.com > file1.txt')
print(command)

os.system('sudo date > /etc/name.txt')

