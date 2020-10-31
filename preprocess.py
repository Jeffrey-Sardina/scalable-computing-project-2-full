import cv2
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import os
import time
from multiprocessing import Pool

'''
Just copy and save new image files
Ref:
    https://techtutorialsx.com/2018/06/02/python-opencv-converting-an-image-to-gray-scale/
'''
def DBgrey_all(source_dir, destination_dir, img_names):
    '''
    Experimental, currently is not consistent
    Also very slow
    '''
    num_total = len(img_names)
    num_done = 0
    for img_name in img_names:
        DBgrey(os.path.join(source_dir, img_name), os.path.join(destination_dir, img_name))
        num_done += 1
        print(num_done, 'of', num_total)

def DBgrey(img_name, dst_name):
    #Collect img as greyscale
    raw_data = cv2.imread(img_name)
    img_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2GRAY)
    rows, columns = img_data.shape
    img_data = np.reshape(img_data, (-1, 1))

    #DBSCAN
    db = DBSCAN()
    db.fit(img_data)

    #Filter noise further into a final image
    std = db.labels_.std()
    mean = db.labels_.mean()
    cuttoff = mean + 0 * std
    db.labels_[db.labels_ > cuttoff] = 255
    db.labels_[db.labels_ < cuttoff] = 0
    processed_image = np.reshape(db.labels_, (rows, columns))

    #Write
    cv2.imwrite(dst_name, processed_image)

def grey_all(source_dir, destination_dir, img_names):
    '''
    Very fast and verified
    '''
    num_total = len(img_names)
    num_done = 0
    for img_name in img_names:
        grey(os.path.join(source_dir, img_name), os.path.join(destination_dir, img_name))
        num_done += 1
        print(num_done, 'of', num_total)

def grey(img_name, dst_name):
    #Collect img as greyscale
    raw_data = cv2.imread(img_name)
    img_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(dst_name, img_data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', help='Source of images to preprocess', type=str)
    parser.add_argument('--destination-dir', help='Destination for preprocessed images', type=str)
    parser.add_argument('--method', help='Preprocessing method to use. Options: grey, DBgrey', type=str)
    args = parser.parse_args()

    if args.source_dir is None:
        print("Please specify the source directory")
        exit(1)

    if args.destination_dir is None:
        print("Please specify the destination directory")
        exit(1)

    if args.method is None:
        print("Please specify preprocessing method")
        exit(1)

    if not os.path.isdir(args.source_dir):
        raise ValueError('Invalid source directory')
    if not os.path.isdir(args.destination_dir):
        raise ValueError('Invalid destination directory')

    start = time.time()
    img_names = [os.path.basename(path) for path in glob.glob(os.path.join(args.source_dir, '*.*'))]
    processes = 8
    pool = Pool(processes=processes)
    img_lists = [img_names[(i * len(img_names)) // processes : ((i + 1) * len(img_names)) // processes] for i in range(processes)]
    
    if args.method == 'DBgrey':
        for l in img_lists:
            pool.apply_async(DBgrey_all, args=(args.source_dir, args.destination_dir, l))
    elif args.method == 'grey':
        for l in img_lists:
            pool.apply_async(grey_all, args=(args.source_dir, args.destination_dir, l))
    
    pool.close()
    pool.join()
    end = time.time()
    print('Time: ' + str(end - start))

if __name__ == '__main__':
    main()

'''
python preprocess.py --source-dir in/base/ --destination-dir in/dbgrey/ --method DBgrey
python preprocess.py --source-dir in/base/ --destination-dir in/grey/ --method grey
'''
