#!/bin/bash

if [[ "$#" -lt 1 ]]
then
    echo 'Please provide the following arguments:'
    echo 'dir and name of the output file for classification (which will be the input for estimating accuracy)'
    echo '1 to generate a new test set or 0 to keep / add to the existing one'
    exit 1
fi

case $2 in
    0)
        echo 'Using existing captchas'
        ;;
    1)
        echo $exitstatus 'Deleting existing captchas and generating new ones'
        rm -r model/est/
        mkdir model/est/
        ;;
    *)
        echo 'invalid arg $1; expected 0 or 1'
        exit 1
esac

python3 generate.py --width 128 --height 64 --length 6 --symbols model/symbols_gen.txt --count 1000 --output-dir model/est/ --processes 8
python3 classify.py --model-name model/model --captcha-dir model/est/ --output $1 --symbols model/symbols.txt --captcha-len 6 --processes 8
python3 estimate_accuracy.py $1
