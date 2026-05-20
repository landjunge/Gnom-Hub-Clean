#!/bin/bash
echo "Starte alle Gnom-Hub Agenten..."
source .venv/bin/activate
set -a
[ -f config/.env ] && source config/.env
set +a

# Alte Agenten killen falls sie noch laufen
pkill -f "python3.*agents\..*AG"
pkill -f "python3.*AG\.py"
sleep 1

# Start in background
python3 -m agents.backupAG > logs/logs_backup.txt 2>&1 &
python3 -m agents.generalAG > logs/logs_general.txt 2>&1 &
python3 -m agents.skillsAG > logs/logs_skills.txt 2>&1 &
python3 -m agents.cronjobAG > logs/logs_cron.txt 2>&1 &
python3 -m agents.watchdogAG > logs/logs_watchdog.txt 2>&1 &
python3 -m agents.soulAG > logs/logs_soul.txt 2>&1 &
python3 -m agents.securityAG > logs/logs_security.txt 2>&1 &

echo "✅ Das Kern-Trio plus General, Backup, Skills, Cronjob, Watchdog, Soul & Security gestartet."
