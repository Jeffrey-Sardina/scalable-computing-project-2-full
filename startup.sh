#!/bin/bash

echo 'Usage: ./startup.sh <input folder> <output file> <optional: recovery id>'
echo '<input folder> is the folder containing all captchas to solve'
echo '<output file> is the file to write classificaitions to'
echo '<recovery id> is the timestsamp of .save files made as the program runs as a back up'
echo '-->in a file a_b_c.save, the timestamp is b'
echo ''

if [[ "$#" -lt 2 ]]
then
    echo 'Please provide the following arguments: input (captcha) folder and output file name'
    exit 1
fi

# echo 'setting up environment'
# source ~/captcha_env/bin/activate

# echo 'attempting to check for and apply updates (timeout 60 seconds)'
# git reset --hard
# timeout 60 git pull
# chmod u+x startup.sh
# exitstatus=$?
# case $exitstatus in
#     124)
#         echo $exitstatus 'failed to get updates, continuing with pre-existing code'
#         ;;
#     125)
#         echo $exitstatus 'timeout command failed'
#         ;;
#     126)
#         echo $exitstatus 'git command cannot be invoked'
#         ;;
#     127)
#         echo $exitstatus 'git command not found'
#         ;;
#     137)
#         echo $exitstatus 'git command sent kill signal'
#         ;;
#     0)
#         echo $exitstatus 'all updates pulled successfully'
#         ;;
#     *)
#         echo $exitstatus 'unknown error'
#         ;;
# esac

# echo 'attempting to update / install needed packages (timeout 300 seconds)'
# timeout 300 python3 install.py

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

if [[ $exitstatus -eq 0 ]]
then
    echo $exitstatus 'classification ended successfully'
else
    echo $exitstatus 'classification failed'
fi
