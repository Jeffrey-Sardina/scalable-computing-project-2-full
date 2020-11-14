'''
https://stackoverflow.com/questions/10549245/how-can-i-adjust-contrast-in-opencv-in-c
https://chrisalbon.com/machine_learning/preprocessing_images/enhance_contrast_of_greyscale_image/
https://stackoverflow.com/questions/42798659/how-to-remove-small-connected-objects-using-opencv
'''

import cv2
import glob
import os
import numpy as np

in_dir = 'in/'
out_dir = 'out/'

def preprocess(fname, out_folder):
    raw_img = cv2.imread(os.path.join(in_dir, fname))
    grey_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
    bw_img = cv2.threshold(grey_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    binary_img = (bw_img == 0)

    #Detect countours
    countour_image = np.zeros(bw_img.shape)
    contours, _ = cv2.findContours(bw_img, cv2.RETR_CCOMP , cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        #https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html
        area = cv2.contourArea(contour)
        if area < 20:
            #https://stackoverflow.com/questions/19222343/filling-contours-with-opencv-python
            cv2.fillPoly(countour_image, pts =[contour], color=255)

    #Masking and final image creation
    countour_mask = (countour_image == 0)
    intensity_mask = (cv2.threshold(grey_img, 100, 255, cv2.THRESH_BINARY)[1] == 0)
    total_mask = countour_mask | intensity_mask
    final_img = binary_img & total_mask
    final_img = np.where(final_img, [0], [255]).astype('float32') 

    cv2.imwrite(os.path.join(out_folder, fname), final_img)

def preprocess_all(folder, out_folder):
    fnames = [os.path.basename(x) for x in glob.glob(os.path.join(folder, '*'))]
    for fname in fnames:
        preprocess(fname, out_folder)

def main():
    preprocess_all(in_dir, out_dir)

if __name__ == '__main__':
    main()