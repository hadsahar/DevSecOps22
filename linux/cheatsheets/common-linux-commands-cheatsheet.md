---
layout: default
title: Common Linux Commands Cheatsheet
---

# Common Linux Commands Cheatsheet

## Common Commands

| Command | Use | Description |
|---|---|---|
| `ls` | List | Lists the current directory and files |
| `ls -R` | List sub directories | Lists files in sub directories also |
| `ls -a` | List hidden files | Lists the current directory including hidden files |
| `ls -al` | List details | Includes details: file size, permissions, owner |
| `cd location` | Change directory | Changes directory to a specified location |
| `cd ..` | Move up one level | Navigates to the parent directory |
| `cd ~` or `cd` | Home | Navigates to the home directory |
| `cd /` | Root directory | Navigates to the root directory |
| `touch filename` | Create file | Creates a file with the designated filename |
| `cat filename` | Display file contents | Displays the content of the designated file |
| `cat file1 file2 > file3` | Combine files | Combines two files (files 1 and 2) into one file (file 3) |
| `mv file "new file path"` | Move file | Moves a file to the designated file path |
| `mv filename new_file_name` | Move and rename file | Moves a file and renames it |
| `sudo` | Superuser do | Execute any command with superuser privileges |
| `rm filename` | Delete file | Deletes the designated file |
| `man <command>` | Help | Shows the help text for a command |
| `history` | Command history | Displays previously used commands |
| `clear` | Clear terminal | Clears all inputs from the terminal |
| `mkdir directoryname` | Make directory | Creates a new directory |
| `rmdir directoryname` | Delete directory | Deletes a directory (must be empty) |
| `mv old_dir new_dir` | Rename directory | Renames a directory |
| `pr -x file` | Divide file | Divides the file into x columns |
| `lpr filename` | Print file | Prints a file |
| `lp -# N filename` | Number of copies | Prints multiple copies of a file |
| `lp -P printername filename` | Specify printer | Prints to a specific printer |
| `apt-get <package>` | Install | Installs the specified package using APT |

## Search Commands

| Command | Use | Description |
|---|---|---|
| `locate file` | Search | Searches the index for a specified file |
| `grep pattern files` | Pattern search | Searches for a specified pattern in designated files |
| `grep -r pattern dir` | Recursive search | Searches the current directory and all subdirectories |
| `grep -i pattern files` | Case insensitive search | Finds matches regardless of case |
| `find /directory -name name` | Find files in a directory | Locates specified files in a specific directory |

## File Permission Commands

| Command | Use | Description |
|---|---|---|
| `ls -l` | List permissions | Lists current permissions (`r`=read `w`=write `x`=execute `-`=no permission) |
| `chown user filename` | Change owner | Changes ownership of a file/directory to the specified user |
| `chown user:group filename` | Change owner and group | Changes both user and group for a file/directory |

## Networking Commands

| Command | Use | Description |
|---|---|---|
| `ssh username@ip-address` or `ssh username@hostname` | Remote login using SSH | Encrypted remote access to a machine |
| `put file` | File upload | Uploads a file to a remote computer using an SSH file transfer client |
| `get file` | File download | Downloads a file from a remote computer using an SSH file transfer client |
| `quit` | Logout | Logs out of the SSH session |
| `ping hostname` or `ping ipaddress` | Ping a device | Uses ICMP to test connectivity |
| `ip a` | List IP information | Shows IP addresses, interfaces, and more |
| `ifconfig` | List IP information | Traditional way to list IP address information |

## Process Commands

| Command | Use | Description |
|---|---|---|
| `bg` | Background | Sends a current process to the background |
| `fg` | Foreground | Brings a background process to the foreground |
| `top` | List processes | Displays details on active processes |
| `ps` | Process status | Shows process status including PID |
| `kill PID` | Kill process | Terminates a process by PID |
| `nice process` | Priority start | Starts a process with a given priority |
| `renice -n N -p PID` | Set priority | Changes the priority of an already running process |
| `df` | List free disk space | Shows free disk space |
| `free` | List RAM usage | Shows RAM usage and available memory |

## Visual Display Editor (VI) Editing Commands

| Command | Use | Description |
|---|---|---|
| `i` | Insert | Insert characters at the cursor location |
| `a` | Insert after cursor | Write characters after the cursor |
| `A` | Insert at end | Inserts characters at the end of the line |
| `Esc` | Exit insert mode | Terminates insert mode |
| `u` | Undo | Undo the last change |
| `U` | Undo all | Undo all changes to the entire line |
| `o` | Open new line | Opens a new line and enters insert mode |
| `dd` | Delete line | Deletes an entire line |
| `3dd` | Delete 3 lines | Deletes 3 lines |
| `D` | Delete after cursor | Deletes content after the cursor to end of line |
| `C` | Delete and insert | Deletes after cursor and enters insert mode |
| `dw` | Delete word | Deletes a word at the cursor location |
| `4dw` | Delete 4 words | Deletes four words |
| `cw` | Change word | Changes a word |
| `x` | Delete character | Deletes a character at the cursor |
| `r` | Replace character | Replaces a single character |
| `R` | Overwrite | Overwrite characters from cursor onward |
| `s` | Substitute character | Substitutes one character then enters insert mode |
| `S` | Substitute line | Substitutes an entire line and enters insert mode |
| `~` | Change case | Changes the case of a single character |
