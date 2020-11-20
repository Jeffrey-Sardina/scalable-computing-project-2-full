#!/bin/bash

#Check cmd args
if [[ "$#" -lt 5 ]]
then
    echo 'Please provide the following arguments:'
    echo 'whether to re-create the training set (0 or 1);'
    echo 'number of training images to create;'
    echo 'number of validation images to create;'
    echo 'number of final model validation images to create;'
    echo 'percent of images that should be monochar;'
    echo '(optional) path of saved model to recover from'
    exit 1
fi

#Re-create training if needed
case $1 in
    0)
        echo 'Using existing captchas'
        ;;
    1)
        echo $exitstatus 'Deleting existing captchas and generating new ones'
        rm -r model/est/
        rm -r model/val/
        rm -r model/gen/
        mkdir model/est/
        mkdir model/val/
        mkdir model/gen/
        ;;
    *)
        echo 'invalid arg $1; expected 0 or 1'
        exit 1
esac

#Generate training, validation, and final validation data
./generate.sh $2 $3 $4 $5

#Create model
case $# in
    5)
        powershell.exe -File train.ps1
        exitstatus=$?
        ;;
    6)
        powershell.exe -File train.ps1 -inputModel $5
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

# #Copy model to pi repo
# cp model/model.tflite ../Tionscadal\ 2\ pi/model/model.tflite

# #Push to git
# cd ../Tionscadal\ 2\ pi/
# eval "$(ssh-agent -s)"
# git add *
# git commit -m "new model"
# git push
