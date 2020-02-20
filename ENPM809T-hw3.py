# Brian Bock
# ENPM809T
# HW 3

#https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
#https://www.pyimagesearch.com/2016/02/22/writing-to-video-with-opencv/
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import datetime
from datetime import datetime
import cv2
from imutils.video import VideoStream
import imutils

start = datetime.now()
# Create dataFile.txt file, which will house all of the timing we record
dataFile=open("dataFile.txt","a+") #a+ for append. Be sure to delete the file from previous runs before starting


# Define the HSV bounds that make the just green light really clear (determined experimentally)
colorLower = (62, 38, 98)
colorUpper = (75, 212, 255)


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1920, 1088)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1920, 1088))

#Define the codec
today = time.strftime("%Y%m%d-%H%M%S")
fps_out = 32
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(today + ".avi", fourcc, fps_out, (1920, 1088))



# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	# Convert the image to HSV space
	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# Thresh the image based on the HSV max/min values
	hsv_binary_image=cv2.inRange(hsv_image, colorLower, colorUpper)

	# Find the contours of the threshed image
	cnts=cv2.findContours(hsv_binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	if len(cnts)>0:
		# Draw the contours on the image
		#contour_image=cv2.drawContours(image, cnts, -1, (0,0,255), 15)


		# Color (B,G,R)
		color = (0, 0, 255) 

		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)

		# Calculate moments of binary image
		M = cv2.moments(c)
		
		if(M["m00"] > 0):
			# Calculate x,y coordinate of center
			x = int(M["m10"] / M["m00"])
			y = int(M["m01"] / M["m00"])
			center_coordinates = (x, y)


			# Line thickness of -1 = filled in 
			thickness = 15

			image = cv2.circle(image, center_coordinates, int(radius), color, thickness)


	#cv2.imshow("Contoured Image", image)
	#cv2.waitKey(0)






	# show the frame
	imagesmall=imutils.resize(image,width=640)
	cv2.imshow("Frame", imagesmall)
	cv2.waitKey(60)
	key = cv2.waitKey(60) & 0xFF

	#save the frame to a file
	out.write(image)
	end = datetime.now()
	warptime=end-start
	print("Finished warp in "+str(warptime)+" (hours:min:sec)")
	dataFile.write(str(warptime)+"\n")

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break