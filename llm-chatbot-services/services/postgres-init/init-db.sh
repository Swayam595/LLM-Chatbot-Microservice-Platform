#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  SELECT 'CREATE DATABASE auth_db'
  WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'auth_db')\gexec

  SELECT 'CREATE DATABASE convo_db'
  WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'convo_db')\gexec
EOSQL
