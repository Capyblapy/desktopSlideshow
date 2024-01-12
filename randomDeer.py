"""Main file for deer project."""

import ctypes
import os
import random
import time
from pathlib import Path

import cv2
import numpy as np
from apscheduler.schedulers.background import BlockingScheduler

import paths

path = paths.path
transition_path = paths.transition_path
video_path = paths.video_path


new_deer = None
old_deer = None

os.listdir(transition_path)

for x in range(len(os.listdir(transition_path))):
    Path.unlink(Path(transition_path / ("frame" + str(x) + ".jpg")))


# First Run
def getnewdeer() -> str:
    """Pick random deer and return it."""
    new_deer = random.choice(os.listdir(path))
    print(new_deer)
    return new_deer


new_deer = getnewdeer()
old_deer = new_deer


def transitiondeer() -> None:
    """Replace blue / green with the deer."""
    # input the code of replacing blue / green with the deer

    video = cv2.VideoCapture(video_path.absolute().as_posix())
    image1 = cv2.imread(Path(path / old_deer).absolute().as_posix())
    image2 = cv2.imread(Path(path / new_deer).absolute().as_posix())

    # Breaking it down

    current_frame = 0
    while True:
        # Capture frame-by-frame
        ret, frame = video.read()

        if not ret:
            break

        # Operate blue
        lower_blue = np.array([70, 70, 70])
        upper_blue = np.array([240, 140, 255])

        copied_image = cv2.resize(image1, (1920, 1080))
        frame = cv2.resize(frame, (1920, 1080))

        mask = cv2.inRange(frame, lower_blue, upper_blue)
        frame[mask != 0] = [0, 0, 0]
        copied_image[mask == 0] = [0, 0, 0]

        frame = copied_image + frame

        # Operate green
        lower_green = np.array([0, 180, 0])
        upper_green = np.array([100, 255, 100])

        copied_image = cv2.resize(image2, (1920, 1080))
        frame = cv2.resize(frame, (1920, 1080))

        mask = cv2.inRange(frame, lower_green, upper_green)
        frame[mask != 0] = [0, 0, 0]
        copied_image[mask == 0] = [0, 0, 0]

        frame = copied_image + frame

        # Saves image of the current frame in jpg file
        name = "./transitionFrames/frame" + str(current_frame) + ".jpg"
        print("Creating..." + name)
        cv2.imwrite(name, frame)

        # To stop duplicate images
        current_frame += 1

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()

    # Playing it
    for x in range(len(os.listdir(transition_path))):
        ctypes.windll.user32.SystemParametersInfoW(
            20,
            0,
            Path(transition_path / ("frame" + str(x) + ".jpg")).absolute().as_posix(),
            0,
        )
        time.sleep(0.1)

    ctypes.windll.user32.SystemParametersInfoW(
        20,
        0,
        Path(path / new_deer).absolute().as_posix(),
        0,
    )

    for x in range(len(os.listdir(transition_path))):
        Path.unlink(Path(transition_path / ("frame" + str(x) + ".jpg")))


transitiondeer()


def deer_swap() -> None:
    """Swap old deer with new deer."""
    new_deer = getnewdeer()
    transitiondeer()

    global old_deer  # noqa: PLW0603
    old_deer = new_deer


# Automatic Run

scheduler = BlockingScheduler()
scheduler.add_job(deer_swap, "interval", minutes=10)
scheduler.start()
