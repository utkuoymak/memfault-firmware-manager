FROM postgres:14.1-alpine
COPY db-seed-files/ /docker-entrypoint-initdb.d/