import numpy as np
# import tensorflow as tf
# from keras.models import load_model
# SingletonMeta


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


def load_all_models():
    all_models = []

    return all_models


class Matcher(metaclass=SingletonMeta):
    def __init__(self):
        self.models = load_all_models()

    def findMatch(self, image):
        img_file = UPLOAD_FOLDER+"/"+image
        print(img_file)

        res = {"result": image}
        return res
