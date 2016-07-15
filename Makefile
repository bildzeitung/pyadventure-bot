# Makefile
#
include mk/postgres.mk

VIRTUALENV=./virtualenv/virtualenv.py

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || $(VIRTUALENV) venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

test: venv/bin/activate
	. ./venv/bin/activate && cd scottadams && python ./setup.py nosetests

all: venv

clean:
	rm -fr venv

.DEFAULT_GOAL = all

.PHONY: venv all clean
