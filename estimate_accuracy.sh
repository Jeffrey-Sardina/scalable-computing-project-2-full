#!/bin/bash

if [[ "$#" -lt 1 ]]
then
    echo 'Please provide the following arguments:'
    echo 'dir and name of the output file for classification (which will be the input for estimating accuracy)'
    exit 1
fi

python3 classify.py --model-name model/model --captcha-dir model/est/ --output $1 --symbols model/symbols.txt --captcha-len 6 --processes 8
python3 estimate_accuracy.py $1
