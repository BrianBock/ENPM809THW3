# Brian Bock
# ENPM809T
# HW 3

# Import required packages
import matplotlib
import matplotlib.pyplot as plt
import numpy as numpy
from datetime import datetime as dtime
import datetime
import time
import statistics

filepath="dataFile.txt"

# Import the data
dataFile = open(filepath,"r")

data=[]

for line in dataFile:
	line=line[:-1] #lines end with "\n", remove
	#print(line)
	data.append(dtime.strptime(line, "%H:%M:%S.%f"))#convert the strings to datetime objects

delta_time=[]

for i in range (0,len(data)-1):
	delta=data[i+1]-data[i]
	delta_ms  = delta / datetime.timedelta(milliseconds=1)
	delta_time.append(delta_ms)
	#print(delta_ms)


plt.hist(delta_time,20,ec='black')
#plt.plot(x,y,label='Original Data')
plt.xlabel('Processing Time (ms)')
plt.ylabel('Number of Frames')
plt.title("Processing Time (No Object in Frame)")

print(statistics.mean(delta_time))

# Create a new figure
plt.figure()
# Create a list of frames (1-len(data))
framecount=list(range(1, len(data)))
plt.plot(framecount,delta_time,'.-')
plt.ylabel('Frame')
plt.xlabel('Processing Time (ms)')
plt.title("Processing Time (No Object in Frame)")

#plt.legend()
plt.show()






