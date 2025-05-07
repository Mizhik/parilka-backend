#!/bin/bash

POSTGRES_USER="your_db_user"
POSTGRES_PASSWORD="your_db_password"
POSTGRES_HOST="localhost"
POSTGRES_PORT=5432
TEST_DB="test_db"

export PGPASSWORD="$POSTGRES_PASSWORD"

echo "Creating test database: $TEST_DB"

createdb -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT $TEST_DB
if [ $? -eq 0 ]; then
  echo "Database '$TEST_DB' created successfully!"
else
  echo "Failed to create database '$TEST_DB'."
  exit 1
fi
