#!/usr/bin/env python3

'''
I have modified this code to allow multiprocessing using:
    https://realpython.com/python-gil/
    https://stackoverflow.com/questions/43749801/how-can-global-variables-be-accessed-when-using-multiprocessing-and-pool?rq=1
    https://docs.python.org/3/library/multiprocessing.html

'''

import os
import numpy
import random
import string
import cv2
import argparse
import captcha.image
from multiprocessing import Pool
import time

args = None
captcha_symbols = None
captcha_generator = None

def generate(it_rng):
    for i in it_rng:
        random_str = ''.join([random.choice(captcha_symbols) for j in range(args.length)])
        image_path = os.path.join(args.output_dir, random_str+'.png')
        if os.path.exists(image_path):
            version = 1
            while os.path.exists(os.path.join(args.output_dir, random_str + '_' + str(version) + '.png')):
                version += 1
            image_path = os.path.join(args.output_dir, random_str + '_' + str(version) + '.png')

        image = numpy.array(captcha_generator.generate_image(random_str))
        cv2.imwrite(image_path, image)

def init_args(local_args, local_captcha_symbols, local_captcha_generator):
    global args, captcha_symbols, captcha_generator
    args = local_args
    captcha_symbols = local_captcha_symbols
    captcha_generator = local_captcha_generator

def main():
    global args, captcha_symbols, captcha_generator

    parser = argparse.ArgumentParser()
    parser.add_argument('--width', help='Width of captcha image', type=int)
    parser.add_argument('--height', help='Height of captcha image', type=int)
    parser.add_argument('--length', help='Length of captchas in characters', type=int)
    parser.add_argument('--count', help='How many captchas to generate', type=int)
    parser.add_argument('--output-dir', help='Where to store the generated captchas', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.width is None:
        print("Please specify the captcha image width")
        exit(1)

    if args.height is None:
        print("Please specify the captcha image height")
        exit(1)

    if args.length is None:
        print("Please specify the captcha length")
        exit(1)

    if args.count is None:
        print("Please specify the captcha count to generate")
        exit(1)

    if args.output_dir is None:
        print("Please specify the captcha output directory")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    captcha_generator = captcha.image.ImageCaptcha(width=args.width, height=args.height)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    if not os.path.exists(args.output_dir):
        print("Creating output directory " + args.output_dir)
        os.makedirs(args.output_dir)

    print("Generating captchas with symbol set {" + captcha_symbols + "}")

    start = time.time()
    processes = 8
    pool = Pool(processes=processes, initializer=init_args, initargs=[args, captcha_symbols, captcha_generator])
    ranges = [range(i * args.count // processes, (i + 1) * args.count // processes) for i in range(processes)]
    for r in ranges:
        pool.apply_async(generate, args=(r,))
    pool.close()
    pool.join()
    end = time.time()
    print('Time: ' + str(end - start))

if __name__ == '__main__':
    main()


'''
python generate.py --width 128 --height 64 --length 5 --symbols model/symbols.txt --count 1500 --output-dir model/gen/
python generate.py --width 128 --height 64 --length 5 --symbols model/symbols.txt --count 150 --output-dir model/val/
'''
