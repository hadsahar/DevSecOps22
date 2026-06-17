# Bash Functions

## Defining a Function

### Syntax 1

```bash
function_name() {
    commands
}
```

### Syntax 2

```bash
function function_name {
    commands
}
```

---

## Calling a Function

```bash
greet() {
    echo "Hello, World!"
}

greet
```

---

## Function Arguments

Arguments are accessed using `$1`, `$2`, etc.

```bash
greet() {
    echo "Hello, $1!"
}

greet "Alice"
greet "Bob"
```

### All arguments

| Variable | Description |
|----------|-------------|
| $1, $2.. | Positional arguments |
| $# | Number of arguments |
| $@ | All arguments as separate words |
| $* | All arguments as a single string |

```bash
show_args() {
    echo "Total args: $#"
    echo "All args: $@"
}

show_args one two three
```

---

## Return Values

Functions return an exit status (0-255). Use `$?` to capture it.

```bash
is_even() {
    if [ $(($1 % 2)) -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

is_even 4
echo $?
```

### Returning strings (use echo)

```bash
get_date() {
    echo $(date +%Y-%m-%d)
}

today=$(get_date)
echo "Today is $today"
```

---

## Local Variables

Use `local` to limit variable scope to the function.

```bash
my_func() {
    local name="Alice"
    echo $name
}

my_func
echo $name   # empty - not accessible outside
```

---

## Recursive Functions

```bash
factorial() {
    if [ $1 -le 1 ]; then
        echo 1
    else
        local prev=$(factorial $(($1 - 1)))
        echo $(($1 * prev))
    fi
}

factorial 5
```

---

## Practical Example: Logging Function

```bash
log() {
    local level=$1
    shift
    local message="$@"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
}

log INFO "Application started"
log ERROR "Connection failed"
```

---
