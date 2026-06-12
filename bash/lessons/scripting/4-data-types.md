# Bash Data Types

## Introduction

Unlike programming languages such as Python or Java, Bash does not have strict data types.

Everything is treated as a string unless used in a numeric context.

---

## Variables

```bash
name="John"
age=30

echo $name
echo $age
```

Output:

```text
John
30
```

---

## String Data

```bash
message="Hello World"

echo "$message"
```

### String Length

```bash
name="DevOps"

echo ${#name}
```

Output:

```text
6
```

---

## Integer Data

```bash
x=10
y=5

echo $((x+y))
echo $((x*y))
```

Output:

```text
15
50
```

---

## Boolean Values

Bash has no real Boolean type.

Convention:

```bash
is_admin=true
is_logged_in=false
```

Example:

```bash
if [ "$is_admin" = true ]; then
    echo "Access granted"
fi
```

---

## Read User Input

```bash
read -p "Enter your name: " username

echo "Hello $username"
```

---

## Environment Variables

```bash
echo $HOME
echo $USER
echo $PATH
```

Create your own:

```bash
export COMPANY="TechCorp"

echo $COMPANY
```

---

## Variable Scope

Global variable:

```bash
name="John"
```

Local variable:

```bash
function hello() {
    local name="David"
    echo $name
}
```

---

