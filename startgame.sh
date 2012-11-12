!/bin/bash

python /data/proc/cactuscanyon/cc.py
  if test $? -eq 42; then
    ./$0
  else
    echo "Quitting"
  fi

