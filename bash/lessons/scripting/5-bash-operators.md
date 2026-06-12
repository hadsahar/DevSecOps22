# Bash Operators

## Arithmetic Operators

| Operator | Description |
|-----------|------------|
| + | Addition |
| - | Subtraction |
| * | Multiplication |
| / | Division |
| % | Modulus |

Example:

```bash
a=10
b=3

echo $((a+b))
echo $((a-b))
echo $((a*b))
echo $((a/b))
echo $((a%b))
```

---

## Assignment Operators

```bash
x=5

((x+=3))
echo $x

((x*=2))
echo $x
```

---

## Comparison Operators

### Numeric

```bash
-eq   equal
-ne   not equal
-gt   greater than
-lt   less than
-ge   greater or equal
-le   less or equal
```

Example:

```bash
if [ 10 -gt 5 ]; then
    echo "True"
fi
```

---

## String Operators

```bash
=
!=
-z
-n
```

Example:

```bash
name="John"

if [ "$name" = "John" ]; then
    echo "Match"
fi
```

---

## Logical Operators

### AND

```bash
if [ $a -gt 5 ] && [ $b -lt 10 ]; then
    echo "True"
fi
```

### OR

```bash
if [ $a -gt 100 ] || [ $b -lt 10 ]; then
    echo "True"
fi
```

### NOT

```bash
if [ ! -f test.txt ]; then
    echo "File not found"
fi
```

---

## File Operators

```bash
-f
-d
-r
-w
-x
```

Example:

```bash
if [ -f file.txt ]; then
    echo "Exists"
fi
```

---

