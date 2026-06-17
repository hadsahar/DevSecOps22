# Bash Loops

## For Loop

### Basic syntax

```bash
for variable in list; do
    commands
done
```

### Example: iterate over a list

```bash
for name in Alice Bob Charlie; do
    echo "Hello, $name"
done
```

### Example: iterate over a range

```bash
for i in {1..5}; do
    echo "Number: $i"
done
```

### Example: C-style for loop

```bash
for ((i=0; i<5; i++)); do
    echo "Index: $i"
done
```

---

## While Loop

### Basic syntax

```bash
while [ condition ]; do
    commands
done
```

### Example: counter

```bash
count=1

while [ $count -le 5 ]; do
    echo "Count: $count"
    ((count++))
done
```

### Example: read file line by line

```bash
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

---

## Until Loop

Runs until the condition becomes true (opposite of while).

```bash
until [ condition ]; do
    commands
done
```

### Example

```bash
num=1

until [ $num -gt 5 ]; do
    echo "Number: $num"
    ((num++))
done
```

---

## Loop Control

### break

Exit the loop immediately.

```bash
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        break
    fi
    echo $i
done
```

### continue

Skip the current iteration and move to the next.

```bash
for i in {1..5}; do
    if [ $i -eq 3 ]; then
        continue
    fi
    echo $i
done
```

---

## Infinite Loop

```bash
while true; do
    echo "Running..."
    sleep 1
done
```

---

## Looping Over Files

```bash
for file in /var/log/*.log; do
    echo "Processing: $file"
done
```

---

## Looping Over Command Output

```bash
for user in $(cat /etc/passwd | cut -d: -f1); do
    echo "User: $user"
done
```

---
