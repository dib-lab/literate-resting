# note: ignore circular dependency warnings.

.SUFFIXES:

all: example.html example.txt.sh

example.txt.sh: ../scan.sh example.txt
	../scan.sh example.txt

example.html: example.txt
	rst2html.py example.txt example.html
