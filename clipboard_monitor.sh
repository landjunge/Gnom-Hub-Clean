#!/bin/bash
last=""
> collected_keys.txt
echo "Starte Clipboard Monitor..."
while true; do
  curr=$(pbpaste)
  if [ "$curr" != "$last" ] && [ -n "$curr" ]; then
    echo "$curr" >> collected_keys.txt
    last="$curr"
  fi
  sleep 0.5
done
