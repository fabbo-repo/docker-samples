#!/bin/sh

set -e

docker cp ./dbexport.pgsql $CONTAINER_NAME:/dbexport.pgsql
docker exec $CONTAINER_NAME sh -c "cat /dbexport.pgsql | psql -U $DB_USER $DB_NAME"

