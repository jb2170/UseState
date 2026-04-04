.PHONY: all
all:

venv:
	python -m venv venv
	./venv/bin/pip install -e .

.PHONY: build
build:
	/usr/bin/python -m build

.PHONY: clean
clean:
	rm -fr -- venv
	rm -fr -- dist src/*.egg-info
