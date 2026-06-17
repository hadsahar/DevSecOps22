# Bash If Statements

## Basic If

```bash
if [ condition ]; then
    commands
fi
```

### Example

```bash
age=20

if [ $age -ge 18 ]; then
    echo "Adult"
fi
```

---

## If-Else

```bash
if [ condition ]; then
    commands
else
    commands
fi
```

### Example

```bash
num=7

if [ $((num % 2)) -eq 0 ]; then
    echo "Even"
else
    echo "Odd"
fi
```

---

## If-Elif-Else

```bash
if [ condition1 ]; then
    commands
elif [ condition2 ]; then
    commands
else
    commands
fi
```

### Example

```bash
score=75

if [ $score -ge 90 ]; then
    echo "A"
elif [ $score -ge 80 ]; then
    echo "B"
elif [ $score -ge 70 ]; then
    echo "C"
else
    echo "F"
fi
```

---

## Nested If

```bash
num=15

if [ $num -gt 0 ]; then
    if [ $((num % 2)) -eq 0 ]; then
        echo "Positive and Even"
    else
        echo "Positive and Odd"
    fi
fi
```

---

## Case Statement

Alternative to multiple if-elif chains.

```bash
case $variable in
    pattern1)
        commands
        ;;
    pattern2)
        commands
        ;;
    *)
        default commands
        ;;
esac
```

### Example

```bash
day="Monday"

case $day in
    Monday)
        echo "Start of week"
        ;;
    Friday)
        echo "Almost weekend"
        ;;
    Saturday|Sunday)
        echo "Weekend!"
        ;;
    *)
        echo "Midweek"
        ;;
esac
```

---

## Test Conditions

### Using [ ] (single bracket)

```bash
if [ "$name" = "admin" ]; then
    echo "Welcome admin"
fi
```

### Using [[ ]] (double bracket - extended)

Supports pattern matching and regex.

```bash
if [[ "$name" == A* ]]; then
    echo "Name starts with A"
fi
```

### Using (( )) for arithmetic

```bash
if (( x > 10 )); then
    echo "x is greater than 10"
fi
```

---

## Combining Conditions

### AND

```bash
if [ $age -ge 18 ] && [ $age -le 65 ]; then
    echo "Working age"
fi
```

### OR

```bash
if [ "$role" = "admin" ] || [ "$role" = "root" ]; then
    echo "Has access"
fi
```

---

## One-Line If

```bash
[ -f /etc/hosts ] && echo "File exists" || echo "File missing"
```

---
