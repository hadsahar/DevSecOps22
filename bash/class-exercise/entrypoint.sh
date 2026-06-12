#!/bin/bash

# Generate training data
/home/student/generate_data.sh

echo ""
echo "=============================================="
echo " DevSecOps Bash Training Lab Ready"
echo "=============================================="
echo ""
echo " Labs directory: ~/labs/"
echo ""
echo " Topics available:"
echo "   navigation/    ls  cd  pwd"
echo "   text/          echo  cat  touch"
echo "   grep/          grep (regex, pipelines)"
echo "   awk/           awk (field processing)"
echo "   sed/           sed (stream editing)"
echo "   cut/           cut (field extraction)"
echo "   sort/          sort (sorting + dedup)"
echo "   head-tail/     head  tail"
echo "   processes/     ps  kill  uptime"
echo "   disk-memory/   df  du  free"
echo "   networking/    ping curl wget ssh rsync"
echo "   archive/       zip  tar"
echo "   permissions/   chmod  chown  chgrp"
echo "   bash-scripting/ variables loops functions arrays cron systemctl"
echo ""
echo " Each subfolder has: exercise.md  (per-command)"
echo " Each topic folder has: HARD_CHALLENGE.md (combined)"
echo ""
echo " Start: ls ~/labs/"
echo ""

exec /bin/bash
