'''
References:
    https://stackoverflow.com/questions/10549245/how-can-i-adjust-contrast-in-opencv-in-c
    https://chrisalbon.com/machine_learning/preprocessing_images/enhance_contrast_of_greyscale_image/
    https://stackoverflow.com/questions/42798659/how-to-remove-small-connected-objects-using-opencv
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
'''

import cv2
import glob
import os
import numpy as np

in_dir = 'in/'
out_dir = 'out/'

def preprocess(fname, out_folder):
    img = cv2.imread(os.path.join(in_dir, fname))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((5,1), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations = 1)

    cuttoff = np.mean(img) - np.std(img)
    img[img > cuttoff] = 255
    img = img.astype('float32')

    cv2.imwrite(os.path.join(out_folder, fname), img)

def preprocess_all(folder, out_folder):
    fnames = [os.path.basename(x) for x in glob.glob(os.path.join(folder, '*'))]
    for fname in fnames:
        preprocess(fname, out_folder)

def main():
    preprocess_all(in_dir, out_dir)

if __name__ == '__main__':
    main()
