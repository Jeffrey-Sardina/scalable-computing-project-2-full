#!/bin/bash

#Check cmd args
if [[ "$#" -lt 1 ]]
then
    echo 'Please provide the following arguments: whether to re-create the training set (0 or 1)'
    exit 1
fi

#Re-create training if needed
if [[ $1 -eq 1 ]]
then
    echo $exitstatus 'Deleting existing captchas and generating new ones'
    rm -r model/est/
    rm -r model/val/
    rm -r model/gen/
    mkdir model/est/
    mkdir model/val/
    mkdir model/gen/
    ./generate.sh
else
    echo $exitstatus 'Using existing captchas'
fi

#Create model
powershell.exe -File train.ps1

#Copy model to pi repo
cp model/model.tflite ../Tionscadal\ 2\ pi/model/model.tflite

#Push to git
cd ../Tionscadal\ 2\ pi/
$ eval "$(ssh-agent -s)"
git add *
git commit -m "new model"
git push
