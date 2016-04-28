# Makefile
#

VIRTUALENV=./virtualenv/virtualenv.py

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || $(VIRTUALENV) venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

all: venv

clean:
	rm -fr venv

.DEFAULT_GOAL = all

.PHONY: all clean
