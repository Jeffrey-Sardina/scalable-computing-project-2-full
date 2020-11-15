#!/bin/bash

$gen=$((100 - ($4 * $1) / 100))
$val=$((100 - ($4 * $2) / 100))
$est=$((100 - ($4 * $3) / 100))

$genMono=$((($4 * $1) / 100))
$valMono=$((($4 * $2) / 100))
$estMono=$((($4 * $3) / 100))

#standard
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $gen --output-dir model/gen/ --processes 8
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $val --output-dir model/val/ --processes 8
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $est --output-dir model/est/ --processes 8

#monochar
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $genMono --output-dir model/gen/ --processes 8 --mono-char 1 
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $valMono --output-dir model/val/ --processes 8 --mono-char 1 
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count $estMono --output-dir model/est/ --processes 8 --mono-char 1 
