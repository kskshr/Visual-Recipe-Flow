#!/usr/bin/env python

import cv2
import sys
import math


if __name__ == "__main__":
    _dir = sys.argv[1]
    fr = 3

    count = 0 
    vidcap = cv2.VideoCapture("{}/video.mp4".format(_dir))

    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    fps = math.ceil(fps / fr) 

    while True:

        success, image = vidcap.read()
        if not success:
            break

        if count % fps == 0:
            cv2.imwrite("{}/frames/frame_{}.jpg".format(_dir, count // fps + 1), image)

        count += 1


