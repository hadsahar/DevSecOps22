---
layout: default
title: Python Lesson 10 - Working with Files
---

# Working with Files in Python

Python provides built-in tools to create, read, write, and manage files on the filesystem. The two main areas covered in this lesson are:

1. **File I/O** — using `open()` with all available modes
2. **OS Module** — interacting with the operating system and filesystem

---

## 1. The `open()` Function

`open()` is Python's built-in function for file operations.

```python
file_object = open(file, mode, encoding=None, errors=None, buffering=-1)
```

| Parameter   | Description                                                        |
|-------------|--------------------------------------------------------------------|
| `file`      | Path to the file (string or path-like object)                      |
| `mode`      | How the file should be opened (see table below)                    |
| `encoding`  | Text encoding (e.g. `"utf-8"`) — only applies to text mode        |
| `errors`    | Error handling strategy (`"strict"`, `"ignore"`, `"replace"`)     |
| `buffering` | Set buffering policy (`-1` = default, `0` = unbuffered for binary) |

---

## 2. File Modes

### Primary Modes

| Mode | Name         | Description                                                                  |
|------|--------------|------------------------------------------------------------------------------|
| `r`  | Read         | Opens for reading. File **must exist**. Default mode.                        |
| `w`  | Write        | Opens for writing. **Creates** file if not found. **Truncates** if exists.   |
| `a`  | Append       | Opens for writing at **end of file**. Creates if not found.                  |
| `x`  | Exclusive    | Creates a **new** file. Raises `FileExistsError` if file already exists.     |

### Modifier Flags (combined with primary modes)

| Flag | Description                                                                 |
|------|-----------------------------------------------------------------------------|
| `t`  | **Text mode** (default). Reads/writes strings. Handles line endings.        |
| `b`  | **Binary mode**. Reads/writes raw bytes. No encoding/newline conversion.    |
| `+`  | **Update mode**. Enables both reading and writing on the same file object.  |

### Combined Mode Summary

| Mode  | Read | Write | Create | Truncate | Start Position |
|-------|------|-------|--------|----------|----------------|
| `r`   | ✅   | ❌    | ❌     | ❌       | Beginning      |
| `r+`  | ✅   | ✅    | ❌     | ❌       | Beginning      |
| `w`   | ❌   | ✅    | ✅     | ✅       | Beginning      |
| `w+`  | ✅   | ✅    | ✅     | ✅       | Beginning      |
| `a`   | ❌   | ✅    | ✅     | ❌       | End            |
| `a+`  | ✅   | ✅    | ✅     | ❌       | End            |
| `x`   | ❌   | ✅    | ✅*    | ❌       | Beginning      |
| `x+`  | ✅   | ✅    | ✅*    | ❌       | Beginning      |
| `rb`  | ✅   | ❌    | ❌     | ❌       | Beginning      |
| `wb`  | ❌   | ✅    | ✅     | ✅       | Beginning      |
| `ab`  | ❌   | ✅    | ✅     | ❌       | End            |
| `rb+` | ✅   | ✅    | ❌     | ❌       | Beginning      |
| `wb+` | ✅   | ✅    | ✅     | ✅       | Beginning      |
| `ab+` | ✅   | ✅    | ✅     | ❌       | End            |

> `✅*` = Creates a new file only — fails if file already exists.

---

## 3. The `with` Statement (Context Manager)

Always use `with` when working with files. It automatically **closes** the file even if an exception occurs.

```python
with open("example.txt", "r") as f:
    content = f.read()
# File is automatically closed here
```

Without `with`, you must close manually:

```python
f = open("example.txt", "r")
content = f.read()
f.close()  # Must be called explicitly
```

---

## 4. Reading Files

### `read()` — Read entire file as one string

```python
with open("example.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

### `readline()` — Read one line at a time

```python
with open("example.txt", "r") as f:
    line = f.readline()
    while line:
        print(line, end="")
        line = f.readline()
```

### `readlines()` — Read all lines into a list

```python
with open("example.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())
```

### Iterating directly (most memory-efficient)

```python
with open("example.txt", "r") as f:
    for line in f:
        print(line.strip())
```

### `read(size)` — Read a specific number of characters

```python
with open("example.txt", "r") as f:
    chunk = f.read(100)  # Read first 100 characters
    print(chunk)
```

---

## 5. Writing Files

### `write()` — Write a string to file

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("Second line\n")
```

> ⚠️ Mode `"w"` truncates the file first. All previous content is lost.

### `writelines()` — Write a list of strings

```python
lines = ["line one\n", "line two\n", "line three\n"]
with open("output.txt", "w") as f:
    f.writelines(lines)
```

> `writelines()` does **not** add newlines automatically — include `\n` in each string.

---

## 6. Appending to Files

```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")
```

Each run adds to the end without deleting existing content.

---

## 7. Creating a File Exclusively (Mode `x`)

```python
try:
    with open("new_file.txt", "x") as f:
        f.write("Created for the first time\n")
except FileExistsError:
    print("File already exists!")
```

---

## 8. Binary Mode

Used for non-text files: images, PDFs, executables, etc.

### Reading a binary file

```python
with open("image.png", "rb") as f:
    data = f.read()
    print(type(data))   # <class 'bytes'>
    print(data[:8])     # First 8 bytes
```

### Writing a binary file (copy example)

```python
with open("source.png", "rb") as src:
    with open("copy.png", "wb") as dst:
        dst.write(src.read())
```

---

## 9. File Object Methods

| Method              | Description                                                        |
|---------------------|--------------------------------------------------------------------|
| `read(size=-1)`     | Read `size` characters/bytes. Default: read entire file.          |
| `readline()`        | Read one line including `\n`.                                      |
| `readlines()`       | Read all lines into a list.                                        |
| `write(s)`          | Write string or bytes `s` to the file.                            |
| `writelines(lines)` | Write a list of strings/bytes.                                     |
| `seek(offset, whence)` | Move cursor. `whence`: `0`=start, `1`=current, `2`=end.       |
| `tell()`            | Return current cursor position (in bytes).                        |
| `flush()`           | Flush internal buffer to OS.                                      |
| `close()`           | Close the file.                                                    |
| `closed`            | Property: `True` if the file is closed.                           |
| `name`              | Property: the file name/path.                                     |
| `mode`              | Property: the mode the file was opened with.                      |

### `seek()` and `tell()` example

```python
with open("example.txt", "r") as f:
    print(f.tell())          # 0 — at the beginning
    f.read(5)                # Read 5 characters
    print(f.tell())          # 5 — cursor moved
    f.seek(0)                # Go back to start
    print(f.read())          # Read everything again
```

---

## 10. Read + Write with `r+` and `w+`

### `r+` — Read and write without truncating

```python
with open("example.txt", "r+") as f:
    content = f.read()
    f.seek(0)
    f.write("OVERWRITTEN start\n")
```

### `w+` — Write and read (truncates first)

```python
with open("example.txt", "w+") as f:
    f.write("Hello\n")
    f.seek(0)
    print(f.read())   # Hello
```

---

## 11. Handling File Exceptions

```python
try:
    with open("missing.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File does not exist.")
except PermissionError:
    print("No permission to access the file.")
except IsADirectoryError:
    print("Expected a file but got a directory.")
except OSError as e:
    print(f"OS error: {e}")
```

---

## 12. The `os` Module

The `os` module provides a way to interact with the operating system — creating directories, listing files, renaming, deleting, navigating paths, and more.

```python
import os
```

---

## 13. Current Working Directory

```python
import os

cwd = os.getcwd()
print(cwd)   # e.g. /Users/username/projects

os.chdir("/tmp")         # Change working directory
print(os.getcwd())       # /tmp
```

---

## 14. Directory Operations

### Create a directory

```python
os.mkdir("new_folder")              # Creates one directory
os.makedirs("parent/child/sub")     # Creates nested directories
```

> `makedirs()` with `exist_ok=True` avoids an error if the directory already exists:

```python
os.makedirs("logs/2024", exist_ok=True)
```

### Remove a directory

```python
os.rmdir("empty_folder")            # Remove empty directory only
```

> To remove a directory tree (non-empty), use `shutil.rmtree()` instead.

### List directory contents

```python
entries = os.listdir(".")           # Returns list of names (files + dirs)
for entry in entries:
    print(entry)
```

### Walk a directory tree

```python
for dirpath, dirnames, filenames in os.walk("."):
    print(f"Directory: {dirpath}")
    for f in filenames:
        print(f"  File: {f}")
```

---

## 15. File Operations with `os`

### Rename / Move a file

```python
os.rename("old_name.txt", "new_name.txt")
```

### Remove a file

```python
os.remove("unwanted.txt")
```

> Raises `FileNotFoundError` if the file doesn't exist.

### Check file/directory existence

```python
print(os.path.exists("example.txt"))   # True or False
print(os.path.isfile("example.txt"))   # True if it's a file
print(os.path.isdir("myfolder"))       # True if it's a directory
```

### Get file size

```python
size = os.path.getsize("example.txt")
print(f"Size: {size} bytes")
```

---

## 16. `os.path` — Path Utilities

```python
import os

path = "/Users/username/projects/app/main.py"

print(os.path.basename(path))      # main.py
print(os.path.dirname(path))       # /Users/username/projects/app
print(os.path.split(path))         # ('/Users/username/projects/app', 'main.py')
print(os.path.splitext(path))      # ('/Users/username/projects/app/main', '.py')

# Join paths safely (handles separators automatically)
full_path = os.path.join("folder", "subfolder", "file.txt")
print(full_path)                   # folder/subfolder/file.txt

# Absolute path
print(os.path.abspath("file.txt")) # /current/working/dir/file.txt
```

---

## 17. Environment Variables

```python
import os

# Get an environment variable (returns None if not set)
home = os.environ.get("HOME")
print(home)   # /Users/username

# Set an environment variable (only for current process)
os.environ["MY_VAR"] = "hello"
print(os.environ["MY_VAR"])   # hello

# List all environment variables
for key, value in os.environ.items():
    print(f"{key} = {value}")
```

---

## 18. Running System Commands with `os`

```python
import os

os.system("ls -la")            # Runs a shell command (UNIX)
os.system("dir")               # Windows equivalent

exit_code = os.system("echo Hello")
print(exit_code)               # 0 = success
```

> For advanced subprocess handling, use the `subprocess` module instead.

---

## 19. File Metadata with `os.stat()`

```python
import os

info = os.stat("example.txt")
print(info.st_size)            # Size in bytes
print(info.st_mtime)           # Last modification time (Unix timestamp)
print(info.st_ctime)           # Creation or metadata change time
print(info.st_mode)            # File permissions (octal)
```

Convert timestamp to readable date:

```python
import os
import datetime

info = os.stat("example.txt")
modified = datetime.datetime.fromtimestamp(info.st_mtime)
print(modified)   # e.g. 2024-04-28 09:15:42
```

---

## 20. `os` vs `pathlib` — Quick Comparison

Python 3.4+ introduced `pathlib` as a more modern, object-oriented alternative to `os.path`.

| Task                  | `os` way                        | `pathlib` way                     |
|-----------------------|---------------------------------|-----------------------------------|
| Current directory     | `os.getcwd()`                   | `Path.cwd()`                      |
| Join paths            | `os.path.join(a, b)`            | `Path(a) / b`                     |
| Check existence       | `os.path.exists(p)`             | `Path(p).exists()`                |
| Is file               | `os.path.isfile(p)`             | `Path(p).is_file()`               |
| Is directory          | `os.path.isdir(p)`              | `Path(p).is_dir()`                |
| Read text file        | `open(p).read()`                | `Path(p).read_text()`             |
| Write text file       | `open(p,"w").write(s)`          | `Path(p).write_text(s)`           |
| File name             | `os.path.basename(p)`           | `Path(p).name`                    |
| Extension             | `os.path.splitext(p)[1]`        | `Path(p).suffix`                  |

---

## 21. Practical Examples

### Example 1 — Word counter

```python
def count_words(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
            words = text.split()
            return len(words)
    except FileNotFoundError:
        return 0

print(count_words("essay.txt"))
```

### Example 2 — Copy a text file line by line

```python
def copy_file(src, dst):
    with open(src, "r", encoding="utf-8") as source:
        with open(dst, "w", encoding="utf-8") as destination:
            for line in source:
                destination.write(line)

copy_file("original.txt", "backup.txt")
```

### Example 3 — Simple logger using append mode

```python
import datetime

def log(message, filepath="app.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

log("Application started")
log("User logged in")
```

### Example 4 — List only `.py` files in a directory

```python
import os

def list_python_files(directory):
    files = []
    for name in os.listdir(directory):
        if name.endswith(".py") and os.path.isfile(os.path.join(directory, name)):
            files.append(name)
    return files

print(list_python_files("."))
```

### Example 5 — Ensure directory exists before writing

```python
import os

def safe_write(filepath, content):
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

safe_write("output/reports/summary.txt", "Report data here")
```

### Example 6 — Read a config file into a dictionary

```python
def read_config(filepath):
    config = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config

# config.txt content:
# host = localhost
# port = 8080
cfg = read_config("config.txt")
print(cfg["host"])   # localhost
```

---