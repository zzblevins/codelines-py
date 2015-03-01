#
# Makefile for codelines.py
#

DATE = `date +%Y%m%d%H%M`

install:
	cp -f codelines.py ~/bin/cl.py

backup:
	cp -f codelines.py /nfs/projnfs/backups/codelines/codelines.py.$(DATE)
	cp -f Makefile /nfs/projnfs/backups/codelines/Makefile.py.$(DATE)
