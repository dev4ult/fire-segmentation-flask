from PIL import Image
import numpy as np
import cv2
import io
from base64 import b64encode


def open_image(file):
    return Image.open(file)


def read_image(file):
    image_np = np.array(open_image(file))
    return cv2.UMat(image_np)


def UMatToPIL(image):
    return Image.fromarray(image.get())


def get_uri(image):
    image_data = image
    data = io.BytesIO()
    image_data.save(data, "JPEG")

    encoded = b64encode(data.getvalue())
    decoded = encoded.decode("utf-8")

    return "data:image/jpeg;base64,%s" % (decoded)
