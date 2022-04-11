#!/usr/bin/env bash

set -o errexit
set -o pipefail

CMD="$@"

function notify() {
  RESET_COLOR='\033[0m'
  case "$1" in
  "ERROR")
    COLOR="\033[1;31m"
    ;;
  "INFO")
    COLOR="\033[1;33m"
    ;;
  "SUCCESS")
    COLOR="\033[1;32m"
    ;;
  "SYS")
    COLOR="\033[1;36m"
    ;;
  *) ;;
  esac
  echo >&2 -e "$COLOR $2 $RESET_COLOR"
}

function checkready_createcluster() {
  notify INFO "[ TRY: CREATE CLUSTER ]"
  su -c 'pg_createcluster --start 13 main -- --auth-local trust --auth-host trust' -m postgres
}

function checkready_postgis() {
  notify INFO "[ TRY: INSTALL POSTGIS EXTENSION ]"
  psql -U postgres -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
}

function checkready_try_connect() {
  python3 <<END
import sys
import psycopg2
import os
try:
    conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

COUNT=0

notify SYS "[ CHECKPOSTGRES START WORK ]"

if checkready_createcluster; then
  notify SUCCESS "[ CLUSTER CREATED ]"
else
  notify ERROR "[ CLUSTER FAILURE ]"
fi

if checkready_postgis; then
  notify SUCCESS "[ POSTGIS EXTENSION INSTALLED ]"
else
  notify ERROR "[ POSTGIS EXTENSION FAILURE ]"
fi

until checkready_try_connect; do
  notify ERROR "[ PSYCOPG2 CONNECT FAILURE ]"
  COUNT=$((COUNT + 1))
  sleep 1
  notify INFO "[ TRY: CONNECT $COUNT \ 10 ]"
  if [ $COUNT -ge 10 ]; then
    notify ERROR "[ CONNECT TESTING TIME OVER ]"
    break
  fi
done

if checkready_try_connect; then
  notify SUCCESS "[ POSTGRES DATABASE IS READY ]"
else
  notify ERROR "[ ALL CONNECTION ATTEMPTS FAILED, PLEASE CHECK CREDINTALS \ CONFIGURATIONS ]"
  exit 1
fi

notify SYS "[ CHECKPOSTGRES END WORK ]"
exec $CMD