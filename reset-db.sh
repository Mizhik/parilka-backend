#!/bin/bash

psql -h localhost -U developer -d parilka -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
