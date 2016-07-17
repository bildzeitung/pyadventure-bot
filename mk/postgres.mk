# Makefile: PostgreSQL bits
#

PG_PATH = $(shell pg_config --bindir)
PG_DIR = $(shell git rev-parse --show-toplevel)/db
PG_DATA = ${PG_DIR}/data
PG_RUN = ${PG_DIR}/run
PG_LOG = ${PG_DIR}/log
PG_PORT = 5432
PG_SOCKET = ${PG_RUN}/.s.PGSQL.${PG_PORT}
PG_PARM = -D ${PG_DATA} -l ${PG_LOG}/pg.log -o "-F -c unix_socket_directories=${PG_RUN} -p ${PG_PORT}"

DB_NAME = development
DB_USER = dev
DB_PWD = test

${PG_DATA}/postgresql.conf:
	mkdir -p ${PG_DATA}
	${PG_PATH}/initdb -D ${PG_DATA} -E UNICODE

${PG_SOCKET}: ${PG_DATA}/postgresql.conf
	mkdir -p ${PG_RUN}
	mkdir -p ${PG_LOG}
	${PG_PATH}/pg_ctl $(PG_PARM) start -w

${PG_DATA}/init: ${PG_SOCKET}
	${PG_PATH}/psql -h ${PG_RUN} -d postgres -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PWD}';"
	${PG_PATH}/createdb -E UTF8 ${DB_NAME} -h ${PG_RUN} -O ${DB_USER}
	touch ${PG_DATA}/init

#
# startup postgres daemon
#
db_start: ${PG_DATA}/init

# 
# shutdown postgres daemon
#
db_stop:
	test -f ${PG_DATA}/postmaster.pid && ${PG_PATH}/pg_ctl $(PG_PARM) stop -m i || true

#
# check status of database
#
db_status:
	@if [ -d "${PG_DIR}" ]; then \
		${PG_PATH}/pg_ctl $(PG_PARM) status ; \
	else \
		echo Database directory not yet made ; \
	fi

#
# shell in to db
#
db_dev: ${PG_SOCKET}
	psql -d postgres://${DB_USER}:${DB_PWD}@localhost:${PG_PORT}/${DB_NAME}

#
# remove database files (shutting the daemon down if necessary)
#
db_clean: db_stop
	rm -fr ${PG_DIR}

.PHONY: db_status db_init db_start db_stop db_clean db_dev
