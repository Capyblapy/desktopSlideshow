import os, random, ctypes,time,cv2
import numpy as np  
from pathlib import Path
from apscheduler.schedulers.background import BlockingScheduler

path = os.path.join(Path.home(), "OneDrive","Desktop", "deerProject", "deer")
newDeer = None 
oldDeer = None

transitionPath = os.path.join(Path.home(), "OneDrive","Desktop", "deerProject", "transitionFrames")
for x in range(0, len(os.listdir(transitionPath))):
    os.remove(os.path.join(transitionPath, "frame"+str(x)+".jpg"))

# First Run
def getNewDeer():
    global newDeer
    newDeer = random.choice(os.listdir(path))
    print(newDeer)

getNewDeer()
oldDeer = newDeer

def transitionDeer():
    # input the code of replacing blue / green with the deer

    video = cv2.VideoCapture(os.path.join(Path.home(), "OneDrive","Desktop", "deerProject", "transition.mp4"))  
    image1 = cv2.imread(os.path.join(path, oldDeer)) 
    image2 = cv2.imread(os.path.join(path, newDeer)) 

    # Breaking it down
        
    currentFrame = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = video.read()

        if not ret: break  

        # Operate (blue)
        lower_blue = np.array([70,70,70])
        upper_blue = np.array([240,140,255])

        copiedImage = cv2.resize(image1, (1920,1080))
        frame = cv2.resize(frame, (1920,1080))

        mask = cv2.inRange(frame, lower_blue, upper_blue)
        frame[mask != 0 ] = [0,0,0]
        copiedImage[mask == 0] = [0,0,0]

        frame = copiedImage + frame

        # Operate (green)
        lower_green = np.array([0,180,0])
        upper_green = np.array([100,255,100])

        copiedImage = cv2.resize(image2, (1920,1080))
        frame = cv2.resize(frame, (1920,1080))

        mask = cv2.inRange(frame, lower_green, upper_green)
        frame[mask != 0 ] = [0,0,0]
        copiedImage[mask == 0] = [0,0,0]

        frame = copiedImage + frame

        # Saves image of the current frame in jpg file
        name = './transitionFrames/frame' + str(currentFrame) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, frame)

        # To stop duplicate images
        currentFrame += 1

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows() 

    # Playing it
    for x in range(0, len(os.listdir(transitionPath))):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(transitionPath, "frame"+str(x)+".jpg"), 0)
        time.sleep(0.1)

    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(path, newDeer), 0)

    for x in range(0, len(os.listdir(transitionPath))):
        os.remove(os.path.join(transitionPath, "frame"+str(x)+".jpg"))

transitionDeer()

def deerSwap():
    getNewDeer()
    transitionDeer()

    global oldDeer
    oldDeer = newDeer

# Automatic Run

scheduler = BlockingScheduler()
scheduler.add_job(deerSwap, 'interval', minutes=10)
scheduler.start() 