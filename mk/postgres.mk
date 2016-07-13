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

${PG_DATA}/postgresql.conf:
	mkdir -p ${PG_DATA}
	${PG_PATH}/initdb -D ${PG_DATA} -E UNICODE

${PG_SOCKET}:
	mkdir -p ${PG_RUN}
	mkdir -p ${PG_LOG}
	${PG_PATH}/pg_ctl $(PG_PARM) start -w

${PG_DATA}/init:
	${PG_PATH}/createdb -E UTF8 development -h ${PG_RUN}
	echo 1 > ${PG_DATA}/init

db_start: ${PG_DATA}/postgresql.conf ${PG_SOCKET} ${PG_DATA}/init

db_stop:
	test -f ${PG_DATA}/postmaster.pid && ${PG_PATH}/pg_ctl $(PG_PARM) stop -m i || true

db_status:
	${PG_PATH}/pg_ctl $(PG_PARM) status

db_dev: ${PG_SOCKET}
	psql -h ${PG_RUN}/ -d development

db_clean: db_stop
	rm -fr ${PG_DIR}

.PHONY: db_status db_init db_start db_stop db_clean db_dev
