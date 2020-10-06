#Import libraries
import cv2
import time
from datetime import datetime
import pandas

first_frame = None
status_list=[None, None]
times = []
df = pandas.DataFrame(columns = ['Start', 'End'])

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status = 0
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)
     
    if first_frame is None:
        first_frame = gray
        continue
    #Delta (change) frame from the 1st frame
    delta_frame = cv2.absdiff(first_frame, gray)
    # Apply a threshold such that it does not capture all the tiny changes
    thresh_frame = cv2.threshold(delta_frame, 75, 255, cv2.THRESH_BINARY)[1]
    # Dilate
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 3)
    # Find contours
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Draw the rectangles:
    for contour in cnts:
        if cv2.contourArea(contour) < 15000:
            continue
        status = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0), 2)
    status_list.append(status)
    status_list = status_list[-2:] #clear all but last 2 items in list
    
    # Save times when an object comes in and goes out of the frame
    if status_list[-1] ==1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] ==0 and status_list[-2] == 1:
        times.append(datetime.now())
    
    # Show the three frames defined above
    cv2.imshow('Gray Frame', gray)
    cv2.imshow('Delta Frame',delta_frame)
    cv2.imshow('Thresholded',thresh_frame)
    cv2.imshow('Color Frame', frame)
    key = cv2.waitKey(1)
    
    if key==ord('q'):
        if status ==1:
            times.append(datetime.now())
        break
# Put the times saved into a dataframe to be used by the plot function
for i in range(0, len(times),2):
    df = df.append({'Start':times[i], 'End': times[i+1]}, ignore_index = True)

# Save to a csv as well for records
df.to_csv('Times.csv')

#Destroy windows when prompted
video.release()
cv2.destroyAllWindows

