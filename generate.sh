#!/bin/bash

#standard
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $((((100 - $4) * $1) / 100)) --output-dir model/gen/ --processes 8
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $((((100 - $4) * $2) / 100)) --output-dir model/val/ --processes 8
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $((((100 - $4) * $3) / 100)) --output-dir model/est/ --processes 8

#monochar
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $1 --output-dir model/gen/ --processes 8 --mono-char 1 
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $2 --output-dir model/val/ --processes 8 --mono-char 1 
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $3 --output-dir model/est/ --processes 8 --mono-char 1 
