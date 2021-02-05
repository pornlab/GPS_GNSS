import cv2 as cv
from PIL import Image
import os
import glonass


class Camera:
    def __init__(self):
        self.cam = None
        self.cam_list = []
        self.BRIGHTNESS = 30
        glonass.check_device()

    def get_list_of_available_cameras(self):
        index = 0
        self.cam_list = []
        while True:
            cap = cv.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                self.cam_list.append(index)
            cap.release()
            index += 1
        return self.cam_list

    def set_camera(self, camera_id):
        self.cam = cv.VideoCapture(camera_id)
        if self.cam:
            return True
        else:
            return False

    def make_a_capture(self, file_path):
        return_value = 0
        image = None
        for i in range(self.BRIGHTNESS):
            return_value, image = self.cam.read()
        self.cam.release()
        cv.imwrite(os.path.join(file_path, 'image.jpg'), image)
        image = Image.open(os.path.join(file_path, "image.jpg"))
        image = image.resize((1280, 1024), Image.ANTIALIAS)
        image.save(os.path.join(file_path, "image.jpg"))
        glonass.set_coordinates(os.path.join(file_path, 'image.jpg'))
        return image
