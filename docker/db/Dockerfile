FROM postgres@sha256:a52a80868bfdd49f90d235a6800c4792f16bf0bd670bab814ad18fb8964a17c7
#Postgres 9.4.5
MAINTAINER Justin Littman <justinlittman@gwu.edu>

ENV PGDATA /sfm-data/postgresql/data
ADD initdb.sql /docker-entrypoint-initdb.d/
