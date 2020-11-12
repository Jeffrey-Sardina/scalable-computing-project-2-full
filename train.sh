#!/bin/bash

python3 train.py --width 128 --height 64 --length 6 --symbols model/symbols.txt --batch-size 32 --epochs 100 --output-model-name model/model_5 --train-dataset model/gen/ --validate-dataset model/val/
