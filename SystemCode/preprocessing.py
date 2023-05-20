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


def resize(image):
    height, width, _ = image.shape
    top, bottom, left, right = 0, 0, 0, 0
    if (height > width):
        left = (height-width)//2
        right = height-width-left
    else:
        top = (width-height)//2
        bottom = width-height-top
    return cv2.copyMakeBorder(image, top,
                              bottom,
                              left,
                              right,
                              cv2.BORDER_CONSTANT,
                              value=(255, 255, 255))


def Pic_preprocessing(file):
    UPLOAD_FOLDER = "./static/images/"
    # Read the image
    image = cv2.imread(UPLOAD_FOLDER+file)

    image = resize(image)
    # Convert the image to grayscale
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a median blur to reduce noise in the image
    blur_img = cv2.medianBlur(gray_img, 5)

    # Detect edges based on color contrast
    canny_img = cv2.Canny(blur_img, 100, 200)

    # Create a white background image
    white_bg = np.ones_like(image) * 255

    # Find contours in the canny image
    contours, hierarchy = cv2.findContours(
        canny_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the white background image
    cv2.drawContours(white_bg, contours, -1, (0, 0, 0), 2)

    result = white_bg

    newname = UPLOAD_FOLDER+"processed_"+file
    cv2.imwrite(newname, result)

    return newname


def Preprocessing_input(image):

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to create a binary image
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE,  # cv2.RETR_EXTERNAL
                                   cv2.CHAIN_APPROX_TC89_L1)  # cv2.CHAIN_APPROX_SIMPLE)

    # Create a white background image with the same shape as the original image
    output = np.ones_like(image) * 255
    output_line = np.ones_like(image) * 255

    # Draw the contours (black lines) on the white background image
    cv2.drawContours(output, contours, -1, (0, 0, 0), thickness=20)
    cv2.drawContours(output_line, contours, -1, (0, 0, 0), thickness=2)

    # Reduce line thickness by eroding the image
    kernel = np.ones((3, 3), np.uint8)
    output = cv2.dilate(output, kernel, iterations=10)

    # Combine output and output_line
    combined_image = cv2.bitwise_and(output, output_line)

    return combined_image


def readImage(image_path):
    return cv2.imread(image_path)


def saveImage(image, image_path):
    cv2.imwrite(image_path, image)
