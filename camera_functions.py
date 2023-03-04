import cv2
import os
import uuid

class camera_function:
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    def get_image(self):
        # reading the input using the camera
        result, image = self.cam.read()

        # If image will detected without any error,
        # show result
        if result:
            upload_name = "upload" + str(uuid.uuid4())
            cv2.imshow(upload_name, image)
            cv2.imwrite(upload_name + ".png", image)
            os.waitKey(0)
            os.destroyWindow(upload_name)

        # If captured image is corrupted, moving to else part
        else:
            print("No image detected. Please! try again")
