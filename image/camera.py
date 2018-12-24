import cv2
import keyboard


class Camera:

    def __init__(self, image_proc):
        self.calibrate = False
        self.lower_skin = []
        self.upper_skin = []
        self.rectangles = []
        self.image = []
        self.roi = []
        self.roi_size = 340
        self.rect_size = 15
        self.nsamples = 6
        self.processor = image_proc
        self.l_offset, self.h_offset = self.processor.initialize_offset()
        self.show_input = True
        self.show_hsv = True
        self.show_mask = True

    def on_press(self, arg):
        self.calibrate = True

    def on_release(self, arg):
        self.calibrate = False
        self.lower_skin, self.upper_skin = self.processor.get_skin_threshold(self.roi, self.rectangles, self.rect_size,
                                                                              self.l_offset, self.h_offset)
        self.rectangles = []

    def draw_calibration_rects(self):
        self.rectangles.append([int(self.roi_size/2), self.rect_size*3])
        self.rectangles.append([int(self.roi_size/2) - self.rect_size*3, self.rect_size*7])
        self.rectangles.append([int(self.roi_size/2) + self.rect_size*3, self.rect_size*7])
        self.rectangles.append([int(self.roi_size/2) - self.rect_size*3, self.rect_size*11])
        self.rectangles.append([int(self.roi_size/2) + self.rect_size*3, self.rect_size*11])
        self.rectangles.append([int(self.roi_size/2), self.rect_size * 13])

        for i in range(self.nsamples):
            cv2.rectangle(self.image, (self.rectangles[i][0], self.rectangles[i][1]),
                          (self.rectangles[i][0] + self.rect_size, self.rectangles[i][1] + self.rect_size), [255, 0, 0])

    def run(self):
        cap = cv2.VideoCapture(0)
        keyboard.on_press_key('c', self.on_press)
        keyboard.on_release_key('c', self.on_release)
        while cap.isOpened():
            ret, self.image = cap.read()
            self.roi = cv2.cvtColor(self.image[0:self.roi_size, 0:self.roi_size, :], cv2.COLOR_BGR2HSV)
            if self.calibrate:
                self.draw_calibration_rects()

            self.image, roi, mask = self.processor.process_image(self.image, self.roi, self.roi_size, self.lower_skin, self.upper_skin)
            if self.show_input:
                cv2.imshow('camera', self.image)
            if self.show_hsv:
                cv2.imshow('hsv', roi)
            if self.show_mask:
                cv2.imshow('mask', mask)
            k = cv2.waitKey(10)
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def set_mute(self, state):
        self.processor.mute = state

    def set_show_input(self, state):
        if state == False:
            cv2.destroyWindow('camera')
        self.show_input = state

    def set_show_hsv(self, state):
        if state == False:
            cv2.destroyWindow('hsv')
        self.show_hsv = state

    def set_show_mask(self, state):
        if state == False:
            cv2.destroyWindow('mask')
        self.show_mask = state

    def set_draw_geometry(self, state):
        self.processor.drawings = state

