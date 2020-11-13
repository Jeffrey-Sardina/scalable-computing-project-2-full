#!/bin/bash

#Check cmd args
if [[ "$#" -lt 1 ]]
then
    echo 'Please provide the following arguments: whether to re-create the training set (0 or 1); (optional) path of saved model to recover from'
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
case $# in
    1)
        powershell.exe -File train.ps1
        exitstatus=$?
        ;;
    2)
        powershell.exe -File train.ps1 -inputModel $2
        exitstatus=$?
        ;;
esac

exitstatus=$?
case $exitstatus in
    0)
        echo $exitstatus 'training succeeded'
        ;;
    *)
        echo $exitstatus 'training failed'
        exit 1
        ;;
esac

#Copy model to pi repo
cp model/model.tflite ../Tionscadal\ 2\ pi/model/model.tflite

#Push to git
cd ../Tionscadal\ 2\ pi/
$ eval "$(ssh-agent -s)"
git add *
git commit -m "new model"
git push
