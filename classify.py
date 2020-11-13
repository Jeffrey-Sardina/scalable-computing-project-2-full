#!/usr/bin/env python3

'''
Reference:
    https://www.tensorflow.org/lite/guide/inference
'''

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import numpy
import string
import random
import argparse
import tflite_runtime.interpreter as tflite
from multiprocessing import Pool
import time
import glob

args = None
captcha_symbols = None
timestamp = None

def decode(characters, y):
    y = numpy.argmax(numpy.array(y), axis=2)[:,0]
    return ''.join([characters[x] for x in y])

def preprocess(raw_data):
    img_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2GRAY)
    image = numpy.array(img_data) / 255.0
    (c, h) = image.shape
    channels = 1
    image = image.reshape([-1, c, h, channels])
    image = image.astype('float32') 
    return image

def init_args(local_args, local_captcha_symbols, start):
    global args, captcha_symbols, timestamp
    args = local_args
    captcha_symbols = local_captcha_symbols
    timestamp = start

def classify(img_div):
    interpreter = tflite.Interpreter(args.model_name+'.tflite')
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    predictions = {}
    uuid = str(random.random()).split('.')[1]
    with open('running_' + str(timestamp) + '_' + uuid + '.save', 'a') as out:
        for x in img_div:
            # load image and process it
            raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
            image = preprocess(raw_data)
            interpreter.set_tensor(input_details[0]['index'], image)
            interpreter.invoke()
            
            prediction = ''
            for i in range(args.captcha_len):
                output_data = interpreter.get_tensor(output_details[i]['index'])[0]
                max_val = 0
                idx = 0
                for i in range(len(output_data)):
                    if output_data[i] >= max_val:
                        max_val = output_data[i]
                        idx = i
                prediction += captcha_symbols[idx]
            predictions[x] = prediction.replace(' ', '')

            #Save results as we go in case there is a power failure
            print(x + ',' + predictions[x], file=out)
    return predictions

def main():
    global args, captcha_symbols

    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    parser.add_argument('--captcha-len', help='Number of symbols (max) per captcha', type=int)
    parser.add_argument('--processes', help='Number of processes to use', type=int)
    parser.add_argument('--continue-from', help='The timestamp of classified data to continue from', type=str)
    args = parser.parse_args()

    if args.model_name is None:
        print("Please specify the CNN model to use")
        exit(1)

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    if args.captcha_len is None:
        print("Please specify the captcha length")
        exit(1)

    if args.processes is None:
        print("Please specify the number of processes to use")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Classifying captchas with symbol set {" + captcha_symbols + "}")

    start = time.time()

    imgs = os.listdir(args.captcha_dir)
    classified = {}

    #If we already have some work done, continue from there
    if args.continue_from is not None:
        img_set = set(imgs)
        classified_img_files = glob.glob('*' + args.continue_from + '*')
        for file_name in classified_img_files:
            with open(file_name, 'r') as inp:
                for line in inp:
                    name, prediction = line.strip().split(',')
                    classified[name] = prediction
        img_set -= classified.keys()
        imgs = [x for x in img_set]

    #Split up the work and run
    pool = Pool(processes=args.processes, initializer=init_args, initargs=[args, captcha_symbols, start])
    img_divs = [imgs[i * len(imgs) // args.processes : (i + 1) * len(imgs) // args.processes] for i in range(args.processes)]
    result = pool.map(classify, img_divs)

    #Save results
    with open(args.output, 'w') as output_file:
        #new classifications
        for mapping in result:
            for key in mapping:
                output_file.write(key + "," + mapping[key] + "\n")

        #Classifications made from before
        if len(classified) > 0:
            for key in classified:
                output_file.write(key + "," + classified[key] + "\n")

    pool.close()

    end = time.time()
    print('Time: ' + str(end - start))

if __name__ == '__main__':
    main()

'''
python classify.py --model-name model/model_2 --captcha-dir in/base/ --output out/model_6t_output.txt --symbols model/symbols.txt --captcha-len 6 --processes 4
'''
