#!/bin/sh

set -e

docker exec $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME > dbexport.pgsql

