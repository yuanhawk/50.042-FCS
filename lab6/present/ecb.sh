#!/bin/sh

echo 'Starting encrypting input sample_enc.txt...'
python3 ecb.py -i sample.txt -o sample_enc.txt -k key -m e
echo 'Completed encrypting output sample_enc.txt...'
echo 'Starting decrypting input sample_enc.txt...'
python3 ecb.py -i sample_enc.txt -o sample_new.txt -k key -m d
echo 'Completed decrypting sample_enc.txt...'