#!/bin/sh

echo 'Starting encrypting input Tux.pbm...'
python3 ecb.py -i Tux.pbm -o Tux_enc.pbm -k key -m e
echo 'Completed encrypting output Tux_enc.pbm...'
echo 'Starting decrypting input Tux_enc.pbm...'
python3 ecb.py -i Tux_enc.pbm -o Tux_new.pbm -k key -m d
echo 'Completed decrypting Tux_new.pbm...'