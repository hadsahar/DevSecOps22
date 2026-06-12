# DevSecOps Bash Training Lab

A Docker-based Linux command-line training environment for practicing essential bash tools.

## What's Inside

| File | Purpose |
|---|---|
| `Dockerfile` | Ubuntu image with all required tools pre-installed |
| `entrypoint.sh` | Startup script — prints the lab menu and drops you into bash |
| `generate_data.sh` | Creates all sample data files under `~/labs/` inside the container |
| `generate_exercises.sh` | Writes `exercise.md` and `HARD_CHALLENGE.md` into each topic folder |
| `tasks.md` | Structured task sheet (8 parts + challenges) |
| `exercise1.md` | Quick in-class exercise sheet |

### Lab Topics (inside the container at `~/labs/`)

```
navigation/     ls  cd  pwd
text/           echo  cat  touch
grep/           grep (regex, pipelines)
awk/            awk (field processing)
sed/            sed (stream editing)
cut/            cut (field extraction)
sort/           sort + dedup
head-tail/      head  tail
processes/      ps  kill  uptime
disk-memory/    df  du  free
networking/     ping  curl  wget  ssh  rsync
archive/        zip  tar
permissions/    chmod  chown  chgrp
bash-scripting/ variables  loops  functions  arrays  cron  systemctl
```

Each topic folder contains:
- Per-command `exercise.md` files
- A `HARD_CHALLENGE.md` combining multiple commands

---

## Requirements

- [Docker](https://docs.docker.com/get-docker/) installed and running

---

## How to Run

### 1. Build the image

```bash
docker build -t bash-training .
```

### 2. Start the lab

```bash
docker run -it bash-training
```

You will land in an interactive bash shell as the `student` user with all lab data already generated.

### 3. Start exploring

```bash
ls ~/labs/
```

Navigate into any topic to find exercises and data:

```bash
ls ~/labs/grep/
cat ~/labs/grep/exercise.md
```

---

## Working Through the Tasks

`tasks.md` is the main guided task sheet. It is divided into 8 parts:

| Part | Topic |
|---|---|
| 1 | `ls` — File system navigation |
| 2 | `cat`, `echo` — Viewing & creating content |
| 3 | `grep` — Searching & filtering |
| 4 | `sort`, `uniq` — Sorting & deduplication |
| 5 | `awk` — Text processing |
| 6 | Piping (`\|`) — Combining commands |
| 7 | `cp`, `mv`, `mkdir` — File operations |
| 8 | Challenge tasks + Bonus aliases |

### Verify Your Work

```bash
# Hidden files (Task 1.2)
ls -la ~ | grep '^\.' | wc -l

# Count "important" in .txt files (Task 3.3)
grep -ri "important" ~/*.txt 2>/dev/null | wc -l

# Unique emails (Task 4.3)
sort email.txt | uniq | wc -l

# Copied .txt files (Task 7.2)
ls backup/*.txt 2>/dev/null | wc -l
```

### Submit Your Work

```bash
tar -czvf completed_exercises.tar.gz ~/backup ~/practice_files ~/myinfo.txt ~/system_report.txt
```

---

## Included Aliases

| Alias | Behavior |
|---|---|
| `lsort` | List files sorted by size, human-readable |
| `cls` | Clear the screen |

---

## Persisting Your Work (Optional)

By default, all changes inside the container are lost when it exits. To keep your work on the host machine, mount a local directory:

```bash
docker run -it -v "$(pwd)/student_work:/home/student/output" bash-training
```

Then copy files to `~/output/` before exiting.
