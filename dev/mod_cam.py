#!/usr/bin/env python
#

import cv2.cv as cv

cv.NamedWindow("RobotVision-3000",cv.CV_WINDOW_AUTOSIZE)
cam = cv.CaptureFromCAM(-1)
cv.SetCaptureProperty(cam,cv.CV_CAP_PROP_FPS,10)

while True:
    feed = cv.QueryFrame(cam)
    cv.ShowImage("RobotVision-3000",feed)
    if cv.WaitKey(100) == 27:
        break

cv.DestroyWindow("RobotVision-3000")


