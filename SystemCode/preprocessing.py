import os
import cv2
import numpy as np


def Contrast(image):

    # converting to LAB color space
    imagelab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(imagelab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return enhanced_img


def Edgeline(image):
    enhanced_img = Contrast(image)

    # Convert to grayscale
    gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)

    # Apply Laplacian filter
    Laplacian = cv2.Laplacian(gray, cv2.CV_32F, ksize=5)
    Laplacian_img = cv2.convertScaleAbs(Laplacian)

    # Apply mean blur and thresholding
    blurred = cv2.blur(Laplacian_img, (3, 3))
    (_, thresh) = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY)

    # Perform morphology operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    r1 = cv2.morphologyEx(closed, cv2.MORPH_CLOSE, np.ones(
        (10, 10), np.uint8), iterations=3)

    # Find edges and draw them on the original image
    edges = cv2.Canny(r1, 50, 150)
    edges = cv2.bitwise_not(edges)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    return edges


def Pic_preprocessing(file):
    UPLOAD_FOLDER = "./static/images/"
    # Read the image
    image = cv2.imread(UPLOAD_FOLDER+file)

    # Convert to grayscale
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    invert = cv2.bitwise_not(grey_img)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(invert, (29, 21), 0)

    # Invert the blurred image
    invertedblur = cv2.bitwise_not(blur)

    # Apply division to create a sketch effect
    sketch = cv2.divide(grey_img, invertedblur, scale=256.0)

    # Convert to BGR (if needed)
    sketch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    enhanced_sketch = Contrast(sketch)

    edges = Edgeline(image)

    # Dilate edges to increase thickness
    kernel = np.ones((10, 10), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    result = cv2.bitwise_and(enhanced_sketch, edges)

    newname = UPLOAD_FOLDER+"processed_"+file
    cv2.imwrite(newname, result)

    return newname
