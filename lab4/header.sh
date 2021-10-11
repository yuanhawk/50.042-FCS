#!/bin/sh

echo 'Starting extract.py'
python3 extract.py -i letter.e -o header_new.pbm -hh header.pbm
echo 'Completed extract.py'