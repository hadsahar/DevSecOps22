---
layout: default
title: Python Lesson 8 - pip and venv
---
# Python Packaging & Environments 

## Table of Contents
1. What is `pip`?
2. What is `venv`?
3. What is PyPI?
4. How They Work Together
5. Creating and Using Virtual Environments
6. Activation (Windows vs Linux/macOS)
7. Installing Packages into a `venv`
8. Deactivating and Deleting Environments
9. Requirements Files
10. Best Practices
11. Cheat Sheet

---

## 1. What is `pip`?

`pip` is Python’s package manager.

It allows you to:
- Install libraries
- Upgrade libraries
- Remove libraries
- Manage dependencies

Example:
```bash
pip install requests
```

##  2. What is venv?
venv (Virtual Environment) is a tool that creates isolated Python environments.

## Why?
- Prevent dependency conflicts
- Use different versions of packages per project
- Keep your global Python clean

### Each venv contains:
- Its own Python interpreter
- Its own pip
- Its own installed packages

## 3. What is PyPI?
PyPI (Python Package Index) is the central repository of Python packages.

`Website: https://pypi.org`
Contains thousands of libraries
pip downloads packages from PyPI by default

## 4. How They Work Together
### Flow:
```bash
PyPI (online registry)
        ↓
     pip install
        ↓
   Virtual Environment (venv)
        ↓
   Your Python Project
```

### Explanation:

You run pip install flask
pip connects to PyPI
Downloads the package
Installs it inside your active venv

Important:
- a. If no venv is active → installs globally
- b. If venv is active → installs locally inside it

## 5. Creating a Virtual Environment
Create a venv
```bash
python -m venv myenv
```
This creates a folder:

myenv/
├── bin/ (Linux/macOS)
├── Scripts/ (Windows)
├── lib/
├── pyvenv.cfg

## 6. Activating the Virtual Environment
### On Windows (CMD)
```bash
myenv\Scripts\activate
```
### On Windows (PowerShell)
```bash
myenv\Scripts\Activate.ps1
```
### On Linux/macOS
```bash
source myenv/bin/activate
```

## 7. What Happens When You Activate?
- Your shell PATH is modified
- python now points to the venv interpreter
- pip installs inside the venv

You will see:
```bash
(myenv) user@machine:~
```

## 8. Installing Packages into the venv
```bash
pip install flask
pip install requests
```

Check installed packages:
```bash
pip list
```

Show details:
```bash
pip show flask
```

## 9. Deactivating the Environment
```bash
deactivate
```
This returns you to the global Python environment.

## 10. Deleting a Virtual Environment
Just delete the folder:
```bash
rm -rf myenv      # Linux/macOS
rmdir /s myenv    # Windows
```

## 11. Requirements Files
Save dependencies:
```bash
pip freeze > requirements.txt
```
Install from file:
```bash
pip install -r requirements.txt
```
Example requirements.txt:
```txt
flask==2.3.2
requests==2.31.0
```

## 12. Best Practices
- Always use venv per project
- Never install packages globally unless necessary
- Use requirements.txt
- Name environments clearly (venv, .venv, env)
- Add venv to .gitignore

Example .gitignore:
```bash
venv/
.env/
```

## 13. Cheat Sheet

```bash
# Create venv
python -m venv myenv
#Activate
    #Windows CMD:
    myenv\Scripts\activate

    #Windows PowerShell:
    myenv\Scripts\Activate.ps1

    #Linux/macOS:
    source myenv/bin/activate

#Install package
pip install package_name

#Upgrade package
pip install --upgrade package_name

#Uninstall package
pip uninstall package_name

#List packages
pip list

#Freeze dependencies
pip freeze > requirements.txt

#Install from requirements
pip install -r requirements.txt

#Deactivate venv
deactivate
