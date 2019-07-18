from django.conf import settings
from celery import shared_task
from celery.signals import worker_process_init
from billiard import current_process

# only load these modules for Celery workers, to not slow down django
if settings.IS_CELERY_WORKER:
    import numpy as np
    import tensorflow as tf
    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.applications.inception_v3 import preprocess_input
    # from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


image_shape = None  # will be initialised in init_gpu()
imagenet_labels = None
base_model = None


# load and preprocess images according to InceptionV3
def loadImage(path):
    img = image.load_img(path, target_size=image_shape[1:3])
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


# return the stringified label of imagenet
def getLabel(index):
    global imagenet_labels
    if imagenet_labels is None:
        labels_path = tf.keras.utils.get_file('ImageNetLabels.txt',
                                              'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
        imagenet_labels = np.array(open(labels_path).read().splitlines())
    return imagenet_labels[index]


def init_gpu():
    global base_model, image_shape
    if base_model is None:
        base_model = tf.keras.applications.InceptionV3(include_top=True,
                                                       weights='imagenet')
        image_shape = base_model.inputs[0].get_shape().as_list()
        print("Worker {} ready".format(current_process().index))


@shared_task
def classify_task(img_path):
    img = loadImage(img_path)
    pred = base_model.predict(img)
    classification = getLabel(pred.argmax())
    print("{:<25} : {}".format(img_path, classification))
    return classification


# replace this function with your own
# returns the classification result of a given image_path
def process_image(img_path):
    task = classify_task.delay(img_path)
    return task.get()


########## INIT ###########

@worker_process_init.connect
def worker_process_init_(**kwargs):
    init_gpu()  # make sure all models are initialized upon starting the worker
