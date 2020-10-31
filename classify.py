#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import numpy
import string
import random
import argparse
import tensorflow as tf
import time

def decode(characters, y):
    y = numpy.argmax(numpy.array(y), axis=2)[:,0]
    return ''.join([characters[x] for x in y])

def preprocess(raw_data):
    #rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
    img_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2GRAY)
    image = numpy.array(img_data) / 255.0
    (c, h, w) = image.shape
    image = image.reshape([-1, c, h, w])
    return image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
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

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Classifying captchas with symbol set {" + captcha_symbols + "}")

    start = time.time()

    #Load model
    interpreter = tf.lite.Interpreter(args.model_name+'.tflite')
    interpreter.allocate_tensors()

    with open(args.output, 'w') as output_file:
        for x in os.listdir(args.captcha_dir):
            # load image and process it
            raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
            image = preprocess(raw_data)
            
            
            prediction = model.predict(image)
            output_file.write(x + "," + decode(captcha_symbols, prediction) + "\n")

            print('Classified ' + x)
    end = time.time()
    print('Time: ' + str(end - start))

if __name__ == '__main__':
    main()

'''
python classify.py --model-name model/model_1 --captcha-dir in/pre/ --output out/model_1_output.txt --symbols model/symbols.txt
'''
