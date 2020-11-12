#!/bin/bash

python3 generate.py --width 128 --height 64 --length 6 --symbols model/no_space.txt --count 33334 --output-dir model/gen/ --processes 8
python3 generate.py --width 128 --height 64 --length 5 --symbols model/no_space.txt --count 33333 --output-dir model/gen/ --processes 8
python3 generate.py --width 128 --height 64 --length 4 --symbols model/no_space.txt --count 33333 --output-dir model/gen/ --processes 8
python3 generate.py --width 128 --height 64 --length 3 --symbols model/no_space.txt --count 33333 --output-dir model/gen/ --processes 8
python3 generate.py --width 128 --height 64 --length 2 --symbols model/no_space.txt --count 33333 --output-dir model/gen/ --processes 8
python3 generate.py --width 128 --height 64 --length 1 --symbols model/no_space.txt --count 33333 --output-dir model/gen/ --processes 8

python3 generate.py --width 128 --height 64 --length 6 --symbols model/no_space.txt --count 8334 --output-dir model/val/ --processes 8
python3 generate.py --width 128 --height 64 --length 5 --symbols model/no_space.txt --count 8333 --output-dir model/val/ --processes 8
python3 generate.py --width 128 --height 64 --length 4 --symbols model/no_space.txt --count 8333 --output-dir model/val/ --processes 8
python3 generate.py --width 128 --height 64 --length 3 --symbols model/no_space.txt --count 8333 --output-dir model/val/ --processes 8
python3 generate.py --width 128 --height 64 --length 2 --symbols model/no_space.txt --count 8333 --output-dir model/val/ --processes 8
python3 generate.py --width 128 --height 64 --length 1 --symbols model/no_space.txt --count 8333 --output-dir model/val/ --processes 8

python3 generate.py --width 128 --height 64 --length 6 --symbols model/no_space.txt --count 834 --output-dir model/est/ --processes 8
python3 generate.py --width 128 --height 64 --length 5 --symbols model/no_space.txt --count 833 --output-dir model/est/ --processes 8
python3 generate.py --width 128 --height 64 --length 4 --symbols model/no_space.txt --count 833 --output-dir model/est/ --processes 8
python3 generate.py --width 128 --height 64 --length 3 --symbols model/no_space.txt --count 833 --output-dir model/est/ --processes 8
python3 generate.py --width 128 --height 64 --length 2 --symbols model/no_space.txt --count 833 --output-dir model/est/ --processes 8
python3 generate.py --width 128 --height 64 --length 1 --symbols model/no_space.txt --count 833 --output-dir model/est/ --processes 8
