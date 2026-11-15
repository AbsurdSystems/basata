# Install these dependencies: sudo apt-get install cc65 srecord
# Adjust the run address to match the .org in the source code

VENV_NAME=.venv
VENV_BIN=./$(VENV_NAME)/bin/
TTY=/dev/ttyACM0
CONFIGFILE=raspnas.cfg
MODE=verify
#SOURCE_FILES := $(shell find ./src -name '*.py')
#OBJECT_FILES := $(SOURCE_FILES:%.py=%.mpy)

PROJECT_CODEFILES=dude.mpy fred.mpy ./phew/phew.py ./phew/server.py

all: backupfiles

backupfiles:
	$(VENV_BIN)python3 ./src/basata.py -m $(MODE) -c $(CONFIGFILE) backup

restorefiles:
	$(VENV_BIN)python3 ./src/basata.py -m $(MODE) -c $(CONFIGFILE) restore

cleanfiles:
	$(VENV_BIN)python3 ./src/basata.py -m $(MODE) -c $(CONFIGFILE) cleanup

purgefiles:
	$(VENV_BIN)python3 ./src/basata.py -m $(MODE) -c $(CONFIGFILE) purge

config:
	$(VENV_BIN)python3 ./src/basata.py createcfg

venv:
	python3 -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate

dependencies:
	$(VENV_BIN)pip install paramiko

uninstall:
	rm -R ./$(VENV_NAME)

clean:
	$(RM) *.o *.lst *.map *.bin *.run *.mon *.c1p *.hex

