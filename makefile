# Install these dependencies: sudo apt-get install cc65 srecord
# Adjust the run address to match the .org in the source code

APP_NAME=basata
SCRIPT_PATH=/usr/local/bin/$(APP_NAME)
BASH_SCRIPT_LOCATION=/usr/bin

VENV_NAME=.venv
VENV_PATH=$(SCRIPT_PATH)/$(VENV_NAME)
VENV_BIN=$(VENV_PATH)/bin


define BASH_SCRIPT
#!/bin/bash
$(VENV_BIN)/python3 $(SCRIPT_PATH)/src/basata.py $$*
endef
export BASH_SCRIPT


all: install

console:
	$(VENV_BIN)/python3

test:
	@echo "$$BASH_SCRIPT" > ./$(APP_NAME).sh

install:
	mkdir -p $(SCRIPT_PATH)
	cp -r ./src $(SCRIPT_PATH)
	python3 -m venv $(VENV_PATH)
	. $(VENV_BIN)/activate
	$(VENV_BIN)/pip install paramiko
	chmod -R 755 $(SCRIPT_PATH)
	@echo "$$BASH_SCRIPT" > $(BASH_SCRIPT_LOCATION)/$(APP_NAME)
	chmod -R 755 $(BASH_SCRIPT_LOCATION)/$(APP_NAME)

upgrade:
	cp -ruv ./src $(SCRIPT_PATH)

uninstall:
	rm -R $(SCRIPT_PATH)
	rm $(BASH_SCRIPT_LOCATION)/$(APP_NAME)



