# 03 - Bash Variables

## Creating Variables

```bash
NAME="John"
```

Access:

```bash
echo $NAME
```

Output:

```text
John
```

---

## Rules

Correct:

```bash
CITY="London"
AGE=25
```

Incorrect:

```bash
NAME = John
```

No spaces around `=`.

---

## User Input

```bash
read NAME

echo $NAME
```

Prompt:

```bash
read -p "Enter your name: " NAME
```

---

## Command Output

```bash
DATE=$(date)

echo $DATE
```

---

## Environment Variables

```bash
echo $HOME
echo $USER
echo $PATH
```

---

## Read Only Variable

```bash
readonly COMPANY="Google"
```

---

## Remove Variable

```bash
unset COMPANY
```
