#!/bin/bash

echo 'Usage: ./startup.sh <input folder> <output file> <optional: recovery id>'
echo '<input folder> is the folder containing all captchas to solve'
echo '<output file> is the file to write classificaitions to'
echo '<recovery id> is the timestsamp of .save files made as the program runs as a back up'
echo '-->in a file a_b_c.save, the timestamp is b'
echo ''

#Check command-line args
if [[ "$#" -lt 2 ]]
then
    echo 'Please provide the following arguments: input (captcha) folder and output file name'
    exit 1
fi

#Source venv
echo 'setting up environment'
source ~/captcha_env/bin/activate

#Pull or update code and echo results
echo 'attempting to check for and apply updates (will timeout and continue on bad connection)'
if [[-d .git]]
then
    git reset --hard
    git pull
    exitstatus=$?
else
    git clone https://artur-hawkwing@bitbucket.org/jeffrey-siothrun/scalable-computing-project-2-pi.git
    exitstatus=$?
fi
chmod u+x startup.sh

case $exitstatus in
    0)
        echo $exitstatus 'all updates pulled successfully'
        ;;
    *)
        echo $exitstatus 'failed to pull updates'
        ;;
esac

#Install or update packages
echo 'attempting to update / install needed packages (will timeout and continue on bad connection)'
python3 install.py

#Classify captchas
echo 'Running classification'
case $# in
    2)
        python3 classify.py --model-name model/model_2 --captcha-dir $1 --output $2 --symbols model/symbols.txt --captcha-len 5 --processes 4
        exitstatus=$?
        ;;
    3)
        python3 classify.py --model-name model/model_2 --captcha-dir $1 --output $2 --symbols model/symbols.txt --captcha-len 5 --processes 4 --continue-from $3
        exitstatus=$?
        ;;
esac

#Echo final results
if [[ $exitstatus -eq 0 ]]
then
    echo $exitstatus 'classification ended successfully'
else
    echo $exitstatus 'classification failed'
fi
