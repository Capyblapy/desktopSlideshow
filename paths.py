import os
from pathlib import Path

try:
    if not os.path.exists(os.path.join(Path.home(),"Desktop", "desktopSlideshow", "transitionFrames")):
        os.makedirs(os.path.join(Path.home(),"Desktop", "desktopSlideshow", "transitionFrames"))
except OSError:
    print ('Error: Creating directory of transitionFrames')

path = os.path.join(Path.home(),"Desktop", "desktopSlideshow", "deer")
transitionPath = os.path.join(Path.home(),"Desktop", "desktopSlideshow", "transitionFrames")
mainPath = os.path.join(Path.home(),"Desktop", "desktopSlideshow")