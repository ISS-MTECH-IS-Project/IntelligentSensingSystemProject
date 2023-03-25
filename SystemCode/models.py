import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16
import tensorflow as tf
from tensorflow.keras import layers
from keras.models import load_model
# SingletonMeta
import os
from os import listdir
from os.path import isfile, isdir, join
from pathlib import Path
from sklearn.neighbors import NearestNeighbors


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


UPLOAD_FOLDER = "./static/images"

CHANNELS = 3  # Keep RGB color channels to match the input format of the model


def preprocess_image(filename):
    images = []

    # preprocess of the input image

    return images

# load models from file


def readImagesFromDir(base_img_path='static/images/processed/'):
    dirs = [d for d in listdir(base_img_path) if isdir(
        join(base_img_path, d)) and not d.startswith('.')]

    print(dirs)

    X, y = [], []

    for d in dirs:
        img_path = base_img_path + d + "/"
        files = [f for f in listdir(img_path) if isfile(join(img_path, f))]
        X = X + [os.path.join(img_path, f)
                 for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        y = y + [d for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        # print(d)

    # data_dir = Path(base_img_path)
    # image_count = len(list(data_dir.glob('*/*.*')))

    return X, y, dirs


def process_image(img_file):
    img = tf.keras.utils.load_img(
        img_file, target_size=None, keep_aspect_ratio=True
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.keras.preprocessing.image.smart_resize(
        img_array, size=(224, 224))
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    img_array = img_array / 255.0

    return img_array


def load_all_models():
    # base_model = VGG16(input_shape=(224, 224, 3),  # Shape of our images
    #                    include_top=False,  # Leave out the last fully connected layer
    #                    weights='imagenet')

    # for layer in base_model.layers:
    #     layer.trainable = False
    #     # print(layer)
    # base_model.summary()
    # x = layers.Flatten()(base_model.output)
    # model = tf.keras.models.Model(base_model.input, x)
    model = load_model("models/self_trained.hdf5")
    model2 = load_model("models/self_trained_c.hdf5")
    return model, model2


def build_feat_dic(model, files):

    features = [model.predict(process_image(f))[0] for f in files]

    return features


class Matcher(metaclass=SingletonMeta):
    def __init__(self):
        self.extractor_model, self.classifier = load_all_models()
        self.files, self.folders, self.classes = readImagesFromDir()
        self.featureDic = build_feat_dic(self.extractor_model, self.files)
        print(len(self.files))
        print(len(self.featureDic))
        self.neigh = NearestNeighbors(n_neighbors=1)
        self.neigh.fit(self.featureDic)

    def findMatch(self, image):
        img_file = UPLOAD_FOLDER+"/"+image
        print(img_file)

        predict_res = self.extractor_model.predict(process_image(img_file))[0]
        classify_res = self.classifier.predict(process_image(img_file))[0]
        score = tf.nn.softmax(classify_res)
        print(score)
        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(self.classes[np.argmax(score)], 100 * np.max(score))
        )

        # print("predict results: ", predict_res)
        nearest = self.neigh.kneighbors([predict_res])
        # print(nearest)
        resImage = self.files[nearest[1][0][0]]
        print(resImage)
        res = {"result": resImage}
        return res
