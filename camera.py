import cv2 as cv
from PIL import Image
import os


class Camera:
    def __init__(self):
        self.cam = None
        self.cam_list = []
        self.BRIGHTNESS = 30

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

    def make_a_capture(self, file_path, file_name):
        return_value = 0
        image = None
        for i in range(self.BRIGHTNESS):
            return_value, image = self.cam.read()
        cv2image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = Image.fromarray(cv2image)
        image.save(os.path.join(file_path, file_name))
        return image

    def video_stream(self):
        return_value, image = self.cam.read()
        cv2image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        return img
