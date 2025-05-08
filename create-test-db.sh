#!/bin/bash

source .env

export PGPASSWORD="$POSTGRES_PASSWORD"

echo "Creating test database: $POSTGRES_TEST_DB"

createdb -U $POSTGRES_USER -h localhost -p $POSTGRES_PORT "$POSTGRES_TEST_DB"
if [ $? -eq 0 ]; then
  echo "Database '$POSTGRES_TEST_DB' created successfully!"
else
  echo "Failed to create database '$TEST_DB'."
  exit 1
fi
