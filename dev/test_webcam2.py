#!/usr/bin/env python
#

#http://stackoverflow.com/questions/12574923/how-to-view-video-stream-in-opencv2-python

import cv2

weblink = "http://10.6.0.164:8090/?action=stream"
cv2.namedWindow("Weblink")

vid = cv2.VideoCapture(weblink)

while True:
    success,img = vid.read()
    cv2.imshow("Weblink",img)
