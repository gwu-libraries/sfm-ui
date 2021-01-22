FROM postgres:9.6

MAINTAINER Laura Wrubel <sfm@gwu.edu>

ENV PGDATA /sfm-db-data/postgresql/9.6/data
ADD initdb.sql /docker-entrypoint-initdb.d/
