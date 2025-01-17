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
import tensorflow.keras as keras
import time
import sys

# Build a Keras model given some parameters
def create_model(captcha_length, captcha_num_symbols, input_shape, model_depth=6, module_size=3): #was 5, 2
    input_tensor = keras.Input(input_shape)
    x = input_tensor
    for i, module_length in enumerate([module_size] * model_depth):
        for j in range(module_length):
            x = keras.layers.Conv2D(32*2**min(i, 3), kernel_size=3, padding='same', kernel_initializer='he_uniform')(x)
            x = keras.layers.BatchNormalization()(x)
            x = keras.layers.Activation('relu')(x)
        x = keras.layers.MaxPooling2D(2)(x)

    x = keras.layers.Flatten()(x)
    x = [keras.layers.Dense(captcha_num_symbols, activation='softmax', name='char_%d'%(i+1))(x) for i in range(captcha_length)]
    model = keras.Model(inputs=input_tensor, outputs=x)

    return model

# A Sequence represents a dataset for training in Keras
# In this case, we have a folder full of images
# Elements of a Sequence are *batches* of images, of some size batch_size
class ImageSequence(keras.utils.Sequence):
    def __init__(self, directory_name, batch_size, captcha_length, captcha_symbols, captcha_width, captcha_height, channels):
        self.directory_name = directory_name
        self.batch_size = batch_size
        self.captcha_length = captcha_length
        self.captcha_symbols = captcha_symbols
        self.captcha_width = captcha_width
        self.captcha_height = captcha_height
        self.channels = channels

        file_list = os.listdir(self.directory_name)
        self.files = dict(zip(map(lambda x: x.split('.')[0], file_list), file_list))
        self.used_files = []
        self.count = len(file_list)

    def __len__(self):
        return int(numpy.floor(self.count / self.batch_size))

    def __getitem__(self, idx):
        X = numpy.zeros((self.batch_size, self.captcha_height, self.captcha_width, 1), dtype=numpy.float32)
        y = [numpy.zeros((self.batch_size, len(self.captcha_symbols)), dtype=numpy.uint8) for i in range(self.captcha_length)]

        for i in range(self.batch_size):
            choose_from = list(self.files.keys())
            if(len(choose_from) == 0):
                break
            random_image_label = random.choice(choose_from)
            random_image_file = self.files[random_image_label]

            # We've used this image now, so we can't repeat it in this iteration
            self.used_files.append(self.files.pop(random_image_label))

            # We have to scale the input pixel values to the range [0, 1] for
            # Keras so we divide by 255 since the image is 8-bit RGB
            raw_data = cv2.imread(os.path.join(self.directory_name, random_image_file))
            rgb_data = preprocess(raw_data)

            processed_data = numpy.array(rgb_data) / 255.0
            processed_data = processed_data.reshape(self.captcha_height, self.captcha_width, self.channels)
            X[i] = processed_data

            # We have a little hack here - we save captchas as TEXT_num.png if there is more than one captcha with the text "TEXT"
            # So the real label should have the "_num" stripped out.
            random_image_label_ints = random_image_label.split('_')[0]

            # We also undo the serlialization to unicode integers to recover the character
            random_image_label = ''
            for uni_int in random_image_label_ints.split('-'):
                random_image_label += chr(int(uni_int))

            for j, ch in enumerate(random_image_label):
                y[j][i, :] = 0
                y[j][i, self.captcha_symbols.find(ch)] = 1

        return X, y

def preprocess(raw_img):
    img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)

    '''
    Rectnagular seems to be best here.
        4,1 leaves a bit too kuch, and anthing above 5,1 starts to eat away at the actual data
    Square reduces actual data to much and his no greater effect on non-data
    '''
    kernel = numpy.ones((5,1), numpy.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations = 1)

    '''
    Setting a constant cuttoff is more simple, but sometimes makes the data diappear
    '''
    cuttoff = numpy.mean(img) - numpy.std(img)
    img[img > cuttoff] = 255
    return img.astype('float32')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', help='Width of captcha image', type=int)
    parser.add_argument('--height', help='Height of captcha image', type=int)
    parser.add_argument('--length', help='Length of captchas in characters', type=int)
    parser.add_argument('--batch-size', help='How many images in training captcha batches', type=int)
    parser.add_argument('--train-dataset', help='Where to look for the training image dataset', type=str)
    parser.add_argument('--validate-dataset', help='Where to look for the validation image dataset', type=str)
    parser.add_argument('--output-model-name', help='Where to save the trained model', type=str)
    parser.add_argument('--input-model', help='Where to look for the input model to continue training', type=str)
    parser.add_argument('--epochs', help='How many training epochs to run', type=int)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    parser.add_argument('--processor', help='GPU or CPU', type=str)
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

    if args.batch_size is None:
        print("Please specify the training batch size")
        exit(1)

    if args.epochs is None:
        print("Please specify the number of training epochs to run")
        exit(1)

    if args.train_dataset is None:
        print("Please specify the path to the training data set")
        exit(1)

    if args.validate_dataset is None:
        print("Please specify the path to the validation data set")
        exit(1)

    if args.output_model_name is None:
        print("Please specify a name for the trained model")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    if args.processor is None or args.processor == 'GPU':
        args.processor = '/device:GPU:0'
    elif args.processor == 'CPU':
        args.processor = '/device:CPU:0'

    captcha_symbols = None
    with open(args.symbols) as symbols_file:
        captcha_symbols = symbols_file.readline()

    # physical_devices = tf.config.experimental.list_physical_devices('GPU')
    # assert len(physical_devices) > 0, "No GPU available!"
    # tf.config.experimental.set_memory_growth(physical_devices[0], True)
    # with tf.device('/device:XLA_CPU:0'):

    start = time.time()
    with tf.device(args.processor):
        channels = 1
        model = create_model(args.length, len(captcha_symbols), (args.height, args.width, channels))

        if args.input_model is not None:
            print('recovering from model ' + args.input_model)
            model.load_weights(args.input_model)

        model.compile(loss='categorical_crossentropy',
                      optimizer=keras.optimizers.Adam(1e-4, amsgrad=True),
                      metrics=['accuracy'])

        model.summary()

        training_data = ImageSequence(args.train_dataset, args.batch_size, args.length, captcha_symbols, args.width, args.height, channels)
        validation_data = ImageSequence(args.validate_dataset, args.batch_size, args.length, captcha_symbols, args.width, args.height, channels)

        callbacks = [keras.callbacks.EarlyStopping(patience=3),
                     # keras.callbacks.CSVLogger('log.csv'),
                     keras.callbacks.ModelCheckpoint(args.output_model_name + '_checkpoint_' + str(time.time()) + '.h5', save_freq="epoch", save_best_only=False)]

        # Save the model architecture to JSON
        with open(args.output_model_name+".json", "w") as json_file:
            json_file.write(model.to_json())

        try:
            model.fit_generator(generator=training_data,
                                validation_data=validation_data,
                                epochs=args.epochs,
                                callbacks=callbacks,
                                use_multiprocessing=True)
        except: #change to general except to always save on a crash
            print('KeyboardInterrupt caught, saving current weights as ' + args.output_model_name+ '_resume.h5')
            model.save_weights(args.output_model_name+'_resume.h5')
            raise

        # Save model in tflite format
        tflite_model = tf.lite.TFLiteConverter.from_keras_model(model).convert()
        with open(args.output_model_name + '.tflite', 'wb') as out:
            out.write(tflite_model)

    end = time.time()
    print('Time: ' + str(end - start))

if __name__ == '__main__':
    main()

'''
see train.sh
'''
