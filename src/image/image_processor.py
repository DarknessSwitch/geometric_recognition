import cv2
import numpy as np
import math


class ImageProcessor:

    def __init__(self, nsamples, event_emitter):
        self.nsamples = nsamples
        self.drawings = True
        self.event_emitter = event_emitter
        self.mute = True

    @staticmethod
    def get_median(a):
        h = np.median(a[2:-2, 2:-2, 0])
        s = np.median(a[2:-2, 2:-2, 1])
        v = np.median(a[2:-2, 2:-2, 2])
        return np.array([h, s, v])

    @staticmethod
    def get_angle(start, end, far):
        a = math.sqrt((start[0]-far[0])**2 + (start[1]-far[1])**2)
        b = math.sqrt((end[0]-far[0])**2 + (end[1]-far[1])**2)
        c = math.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)

        angle = math.acos((a*a + b*b - c*c)/(2*a*b)) * 57.2958
        return angle

    @staticmethod
    def get_mask(roi, roi_size, l, u):
        result = np.zeros((roi_size, roi_size, 1), dtype=np.uint8)
        for i in range(len(l)):
            mask = cv2.inRange(roi, l[i], u[i])
            result = cv2.bitwise_or(mask, result)
        return result

    @staticmethod
    def predict(areacnt, areahull, ndefects, shape_rel):
        result = ''
        if ndefects == 0:
            if areacnt/areahull >= 0.85:
                if shape_rel < 0.76:
                    result = 'Palm'
                else:
                    result = 'Fist'
            else:
                result = '1'
        elif ndefects == 4:
            result = '5'
        elif ndefects == 3:
            result = '4'
        elif ndefects == 2:
            result = '3'
        elif ndefects == 1:
            result = '2'
        return result

    def predict_image(self, img, mask):
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            cnt = max(contours, key=lambda x: cv2.contourArea(x))
            eps = 0.003 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, eps, True)
            moments = cv2.moments(approx)
            # cx = 0
            # cy = 0
            # if moments['m00'] != 0:
            #     cx = int(moments['m10'] / moments['m00'])  # cx = M10/M00
            #     cy = int(moments['m01'] / moments['m00'])  # cy = M01/M00
            hull = cv2.convexHull(approx)
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(approx)
            x, y, w, h = cv2.boundingRect(approx)
            shape_rel = min(w,h)/max(w,h)

    # draw shapes for visual representation:
            if self.drawings:
                # cv2.circle(img, (cx, cy), 5, [0, 0, 255], 2)
                cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)
                cv2.drawContours(img, [hull], 0, (0, 0, 255), 2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
                # img = cv2.line(img, (cx, cy), rect_point, [255, 0, 0])
                # img = cv2.circle(img, (cx, cy), int(rect_dist), [255, 255, 255])
                img = cv2.putText(img, '{0:.2}'.format(shape_rel), (img.shape[1] - 200, 150), 1, 2, [0, 0, 255], 2)
    # end draw shapes

            conv_defects = cv2.convexityDefects(approx, cv2.convexHull(approx, returnPoints=False))
            ndefects = 0
            if conv_defects is not None:
                for i in range(conv_defects.shape[0]):
                    s, e, f, d = conv_defects[i, 0]
                    start = tuple(approx[s][0])
                    end = tuple(approx[e][0])
                    far = tuple(approx[f][0])

                    # cv2.circle(img, end, 5, [255, 0, 255], -1)
                    # if self.drawings:
                    #     cv2.line(img, start, end, [255, 255, 0], 2)
                    angle = self.get_angle(start, end, far)
                    # cv2.putText(img, 'A', start, 1, 1, [0, 0, 255])
                    # cv2.putText(img, 'B', tuple(approx[max(s-15, 0)][0]), 1, 1, [0, 255, 255])
                    # cv2.putText(img, 'C', tuple(approx[min(s+15, len(approx)-1)][0]), 1, 1, [255, 0, 0])
                    #     cv2.circle(img, start, 5, [255, 255, 0], -1)
                    if d > 15000 and angle < 90:
                        # cv2.putText(img, '{0:.2f}'.format(angle), far, 1, 1, [0, 0, 255])
                        if self.drawings:
                            cv2.circle(img, far, 5, [0, 0, 255], -1)
                        ndefects = ndefects + 1
            prediction = self.predict(areacnt, areahull, ndefects, shape_rel)
            if not self.mute:
                self.event_emitter.emit(self.event_emitter.event_name, prediction)
            img = cv2.putText(img, prediction, (img.shape[1] - 200, 50), 1, 2, [0, 0, 255], 2)
            return img

    def get_skin_threshold(self, roi, rectangles, rect_size, l_offset, h_offset):
        l_tresholds = []
        u_tresholds = []
        for i in range(self.nsamples):
            rect = roi[rectangles[i][0]:rectangles[i][0] + rect_size,
                   rectangles[i][1]:rectangles[i][1] + rect_size, :]

            median = self.get_median(rect)
            l_tresholds.append([max(median[0] - l_offset[0], 0), max(median[1] - l_offset[1], 0),
                                max(median[2] - l_offset[2], 0)])
            u_tresholds.append([min(median[0] + h_offset[0], 255), min(median[1] + h_offset[1], 255),
                                min(median[2] + h_offset[2], 255)])

        return np.array(l_tresholds, dtype=np.uint8), np.array(u_tresholds, dtype=np.uint8)

    def process_image(self, image, roi, roi_size, l_thres, u_thres):
        img = cv2.rectangle(image, (0, 0), (roi_size, roi_size), [0, 255, 0], 2)
        img = cv2.putText(img, 'Hold \'c\' to calibrate skin color', (10, roi_size+30), 2, 1, [0, 0, 255])
        # ret, rectangle = cv2.threshold(rectangle, 70, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        roi = cv2.medianBlur(roi, 9)
        mask = self.get_mask(roi, roi_size, l_thres, u_thres)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
        mask = cv2.medianBlur(mask, 5)
        mask = cv2.dilate(mask, kernel, iterations=1)
        self.predict_image(img, mask)
        return img, roi, mask

    def initialize_offset(self):
        low = [15, 30, 60]
        high = [7, 40, 60]

        return low, high
