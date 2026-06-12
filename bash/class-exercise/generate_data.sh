#!/bin/bash
# =============================================================================
# DevSecOps Lab Environment Builder
# Run as: bash generate_data.sh
# Creates: /home/student/labs/<topic>/<subtopic>/ with exercises + data files
# =============================================================================
set -e
BASE=/home/student/labs
echo "[+] Building DevSecOps lab environment under $BASE ..."

# ─── NAVIGATION (ls, cd, pwd) ─────────────────────────────────────────────────
mkdir -p "$BASE/navigation/ls" "$BASE/navigation/cd" "$BASE/navigation/pwd"
mkdir -p "$BASE/navigation/data/projects/devops" "$BASE/navigation/data/projects/python"
mkdir -p "$BASE/navigation/data/logs" "$BASE/navigation/data/archive/2024/jan" "$BASE/navigation/data/archive/2024/feb"
for i in 1 2 3; do echo "project $i content" > "$BASE/navigation/data/projects/devops/project$i.txt"; done
touch "$BASE/navigation/data/.secret" "$BASE/navigation/data/.env_sample" "$BASE/navigation/data/.hidden_notes"
dd if=/dev/urandom bs=1024 count=50 2>/dev/null | base64 > "$BASE/navigation/data/large_file.bin"
echo "jan backup data" > "$BASE/navigation/data/archive/2024/jan/backup.log"
echo "feb backup data" > "$BASE/navigation/data/archive/2024/feb/backup.log"

# ─── TEXT TOOLS (echo, cat, touch) ────────────────────────────────────────────
mkdir -p "$BASE/text/echo" "$BASE/text/cat" "$BASE/text/touch"
cat > "$BASE/text/cat/part1.txt" <<'EOF'
DevOps is culture
Automation is key
Infrastructure as code
EOF
cat > "$BASE/text/cat/part2.txt" <<'EOF'
CI/CD pipelines
Docker containers
Kubernetes orchestration
EOF

# ─── GREP ─────────────────────────────────────────────────────────────────────
mkdir -p "$BASE/grep"
cat > "$BASE/grep/access.log" <<'EOF'
2024-01-15 08:01:32 ERROR   [auth]    Login failed for user admin from 192.168.1.10
2024-01-15 08:02:11 INFO    [web]     GET /index.html 200 OK
2024-01-15 08:05:44 WARNING [disk]    Disk usage at 85% on /dev/sda1
2024-01-15 08:10:01 ERROR   [db]      Database connection timeout after 30s
2024-01-15 08:11:23 INFO    [web]     POST /api/login 200 OK
2024-01-15 08:15:55 ERROR   [auth]    Login failed for user root from 10.0.0.5
2024-01-15 08:20:00 WARNING [mem]     Memory usage at 92%
2024-01-15 08:25:10 INFO    [deploy]  Deployment pipeline started for build #442
2024-01-15 08:26:33 INFO    [deploy]  Build #442 passed all tests
2024-01-15 08:27:01 ERROR   [deploy]  Build #442 deployment FAILED rollback triggered
2024-01-15 08:30:00 INFO    [cron]    Nightly backup job started
2024-01-15 08:35:00 INFO    [cron]    Nightly backup completed successfully
EOF
cat > "$BASE/grep/emails.txt" <<'EOF'
john.doe@gmail.com
sarah.smith@yahoo.com
mike@company.com
john.doe@gmail.com
devops@student.io
admin@linux.org
noreply@github.com
sarah.smith@yahoo.com
root@localhost
EOF
cat > "$BASE/grep/code_sample.py" <<'EOF'
import os
def login(username, password):
    # TODO: implement real auth
    if username == "admin" and password == "secret123":
        return True
    return False
def logout(username):
    print(f"User {username} logged out")
if __name__ == "__main__":
    user = os.getenv("APP_USER", "guest")
    login(user, "password")
EOF

# ─── AWK ──────────────────────────────────────────────────────────────────────
mkdir -p "$BASE/awk"
cat > "$BASE/awk/employees.csv" <<'EOF'
ID,Name,Department,Salary,City
1,Alice,DevOps,7500,TelAviv
2,Bob,Backend,6200,Haifa
3,Carol,Frontend,5800,Jerusalem
4,David,DevOps,8100,TelAviv
5,Eve,Security,9000,Haifa
6,Frank,Backend,6500,TelAviv
7,Grace,DevOps,7200,Jerusalem
8,Hank,Frontend,5500,Haifa
EOF
cat > "$BASE/awk/server_stats.txt" <<'EOF'
web01   cpu=45%  mem=62%  disk=30%
web02   cpu=88%  mem=91%  disk=72%
db01    cpu=22%  mem=55%  disk=85%
db02    cpu=67%  mem=78%  disk=90%
cache01 cpu=15%  mem=30%  disk=10%
EOF

# ─── SED ──────────────────────────────────────────────────────────────────────
mkdir -p "$BASE/sed"
cat > "$BASE/sed/config.ini" <<'EOF'
[database]
host=localhost
port=5432
user=dbadmin
password=changeme123
db_name=production

[web]
host=0.0.0.0
port=8080
debug=true
log_level=INFO

[cache]
host=localhost
port=6379
ttl=3600
EOF
cat > "$BASE/sed/template.html" <<'EOF'
<html>
<head><title>TITLE_PLACEHOLDER</title></head>
<body>
  <h1>Welcome, USERNAME!</h1>
  <p>Role: USER_ROLE | Env: ENV_NAME | Version: APP_VERSION</p>
</body>
</html>
EOF

# ─── CUT ──────────────────────────────────────────────────────────────────────
mkdir -p "$BASE/cut"
cat > "$BASE/cut/passwd_sample.txt" <<'EOF'
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
student:x:1000:1000:Student User:/home/student:/bin/bash
devops:x:1001:1001:DevOps Engineer:/home/devops:/bin/bash
EOF
cat > "$BASE/cut/services.csv" <<'EOF'
service_name,port,protocol,status,description
nginx,80,TCP,running,Web server
postgres,5432,TCP,running,Database
redis,6379,TCP,running,Cache store
ssh,22,TCP,running,Secure shell
prometheus,9090,TCP,stopped,Monitoring
grafana,3000,TCP,running,Dashboard
EOF

# ─── SORT ─────────────────────────────────────────────────────────────────────
mkdir -p "$BASE/sort"
cat > "$BASE/sort/scores.txt" <<'EOF'
Alice 92
Bob 78
Carol 95
David 61
Eve 88
Frank 95
Grace 73
Hank 61
EOF
cat > "$BASE/sort/mixed.txt" <<'EOF'
banana
Apple
cherry
apple
Banana
CHERRY
date
EOF
cat > "$BASE/sort/versions.txt" <<'EOF'
1.9.2
1.10.0
2.0.1
1.9.11
1.2.0
EOF

# ─── HEAD & TAIL ──────────────────────────────────────────────────────────────
mkdir -p "$BASE/head-tail"
for i in $(seq 1 200); do
    level=$([ $((i % 5)) -eq 0 ] && echo "ERROR" || ([ $((i % 3)) -eq 0 ] && echo "WARNING" || echo "INFO"))
    echo "2024-01-15 $(printf '%02d' $((i/60))):$(printf '%02d' $((i%60))):00 $level [svc] Log entry number $i" >> "$BASE/head-tail/big.log"
done

# ─── PROCESSES (ps, kill, uptime) ─────────────────────────────────────────────
mkdir -p "$BASE/processes/ps" "$BASE/processes/kill" "$BASE/processes/uptime"

# ─── DISK & MEMORY (df, du, free) ─────────────────────────────────────────────
mkdir -p "$BASE/disk-memory/df" "$BASE/disk-memory/du/subdir" "$BASE/disk-memory/free"
dd if=/dev/zero bs=1024 count=100 2>/dev/null > "$BASE/disk-memory/du/file_100k.bin"
dd if=/dev/zero bs=1024 count=500 2>/dev/null > "$BASE/disk-memory/du/file_500k.bin"
dd if=/dev/zero bs=1024 count=1024 2>/dev/null > "$BASE/disk-memory/du/file_1m.bin"
dd if=/dev/zero bs=1024 count=200 2>/dev/null > "$BASE/disk-memory/du/subdir/file_200k.bin"

# ─── NETWORKING (ping, curl, wget, ssh, rsync) ────────────────────────────────
mkdir -p "$BASE/networking/ping" "$BASE/networking/curl" "$BASE/networking/wget"
mkdir -p "$BASE/networking/ssh" "$BASE/networking/rsync"

# ─── ARCHIVE (zip, tar) ───────────────────────────────────────────────────────
mkdir -p "$BASE/archive/zip" "$BASE/archive/tar"
mkdir -p "$BASE/archive/data/project/src" "$BASE/archive/data/project/docs" "$BASE/archive/data/project/tests"
echo "main app code"       > "$BASE/archive/data/project/src/app.py"
echo "utility functions"   > "$BASE/archive/data/project/src/utils.py"
echo "# Project Docs"      > "$BASE/archive/data/project/docs/README.md"
echo "unit tests here"     > "$BASE/archive/data/project/tests/test_app.py"
echo "flask==2.3.0"        > "$BASE/archive/data/project/requirements.txt"

# ─── PERMISSIONS (chmod, chown, chgrp) ────────────────────────────────────────
mkdir -p "$BASE/permissions/chmod" "$BASE/permissions/chown" "$BASE/permissions/chgrp"
echo "DB_PASS=supersecret"  > "$BASE/permissions/chmod/secret.txt"
echo "Public info here"     > "$BASE/permissions/chmod/public.txt"
echo "#!/bin/bash"          > "$BASE/permissions/chmod/script.sh"
echo "server.port=8080"     > "$BASE/permissions/chmod/readonly.cfg"
chmod 600 "$BASE/permissions/chmod/secret.txt"
chmod +x  "$BASE/permissions/chmod/script.sh"
chmod 444 "$BASE/permissions/chmod/readonly.cfg"

# ─── BASH SCRIPTING ───────────────────────────────────────────────────────────
mkdir -p "$BASE/bash-scripting/syntax"
mkdir -p "$BASE/bash-scripting/variables-datatypes"
mkdir -p "$BASE/bash-scripting/operators"
mkdir -p "$BASE/bash-scripting/if-else"
mkdir -p "$BASE/bash-scripting/loops"
mkdir -p "$BASE/bash-scripting/functions"
mkdir -p "$BASE/bash-scripting/arrays"
mkdir -p "$BASE/bash-scripting/cron"
mkdir -p "$BASE/bash-scripting/systemctl"

# ─── GENERATE EXERCISE FILES ──────────────────────────────────────────────────
echo "[+] Writing exercise files..."
bash "$(dirname "$0")/generate_exercises.sh" "$BASE"

echo ""
echo "[+] Lab structure created:"
find "$BASE" -maxdepth 3 -type d | sed 's|'"$BASE"'||' | sort
echo ""
echo "[+] Done! Start with: ls $BASE"
