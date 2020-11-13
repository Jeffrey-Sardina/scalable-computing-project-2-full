python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols.txt --count 200000 --output-dir model/gen/ --processes 8
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols.txt --count 50000 --output-dir model/val/ --processes 8
python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols.txt --count 5000 --output-dir model/est/ --processes 8
