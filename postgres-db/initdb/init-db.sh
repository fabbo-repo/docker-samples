#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE keycloakdb;
    CREATE USER keycloak_user WITH PASSWORD '${KEYCLOAK_USER_PASSWORD}';
    GRANT ALL PRIVILEGES ON DATABASE keycloakdb TO keycloak_user;
    ALTER DATABASE keycloakdb OWNER TO keycloak_user;

    CREATE DATABASE currencydb;
    CREATE USER currency_api_user WITH PASSWORD '${CURRENCY_USER_PASSWORD}';
    GRANT ALL PRIVILEGES ON DATABASE currencydb TO currency_api_user;
    ALTER DATABASE currencydb OWNER TO currency_api_user;
EOSQL
