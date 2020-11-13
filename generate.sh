python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols.txt --count $1 --output-dir model/gen/ --processes 8
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols.txt --count $2 --output-dir model/val/ --processes 8
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols.txt --count $3 --output-dir model/est/ --processes 8
