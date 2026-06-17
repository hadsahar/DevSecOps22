# Read and User Input

## Basic Read

```bash
read variable
```

### Example

```bash
echo "Enter your name:"
read name
echo "Hello, $name"
```

---

## Read with Prompt (-p)

```bash
read -p "Enter your age: " age
echo "You are $age years old"
```

---

## Read Multiple Variables

```bash
read -p "Enter first and last name: " first last
echo "First: $first"
echo "Last: $last"
```

---

## Read with Default Value

```bash
read -p "Enter port [8080]: " port
port=${port:-8080}
echo "Using port: $port"
```

---

## Read with Timeout (-t)

```bash
read -t 5 -p "Enter value (5 sec timeout): " value

if [ -z "$value" ]; then
    echo "Timed out, using default"
fi
```

---

## Read Single Character (-n)

```bash
read -n 1 -p "Continue? (y/n): " answer
echo
if [ "$answer" = "y" ]; then
    echo "Continuing..."
fi
```

---

## Silent Input with stty -echo

Use `stty -echo` to hide user input (useful for passwords).

```bash
echo "Enter password:"
stty -echo
read password
stty echo
echo
echo "Password saved (hidden from terminal)"
```

---

## Read with -s Flag (Silent)

The `-s` flag does the same as `stty -echo` but built into `read`.

```bash
read -sp "Enter password: " password
echo
echo "Password length: ${#password}"
```

---

## stty Options

| Command | Description |
|---------|-------------|
| stty -echo | Disable terminal echo (hide input) |
| stty echo | Re-enable terminal echo |
| stty -icanon | Disable canonical mode (read char by char) |
| stty icanon | Re-enable canonical mode |
| stty sane | Reset terminal to default settings |

---

## Practical Example: Login Script

```bash
#!/bin/bash

read -p "Username: " username

stty -echo
read -p "Password: " password
stty echo
echo

if [ "$username" = "admin" ] && [ "$password" = "secret" ]; then
    echo "Access granted"
else
    echo "Access denied"
fi
```

---

## Practical Example: SSH Key Passphrase

```bash
#!/bin/bash

read -p "Enter key name: " keyname

stty -echo
read -p "Enter passphrase: " pass
echo
read -p "Confirm passphrase: " pass_confirm
stty echo
echo

if [ "$pass" != "$pass_confirm" ]; then
    echo "Passphrases do not match!"
    exit 1
fi

echo "Generating key: $keyname"
```

---

## Read from File

```bash
while IFS= read -r line; do
    echo "Line: $line"
done < config.txt
```

---

## Read with Delimiter (-d)

```bash
read -d ":" field1 <<< "hello:world"
echo "$field1"
```

---

## Read into Array (-a)

```bash
read -a fruits -p "Enter fruits (space separated): "
echo "First fruit: ${fruits[0]}"
echo "All fruits: ${fruits[@]}"
```

---
