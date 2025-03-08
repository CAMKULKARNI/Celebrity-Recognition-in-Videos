from copy import deepcopy
from os import listdir, makedirs, path
from shutil import copy, rmtree

from cv2 import imread
from numpy import array, mean
from scipy.signal import argrelmax


def function(workingDirectory, imageFolderName, newFolderName, percentKeyFrames=0.1):
    location = path.join(workingDirectory, imageFolderName)
    images = sorted([image for image in listdir(location)],
                    key=lambda x: int(x[5:-4]))
    xval = []
    yval = []
    for image in images:
        imageLocation = path.join(location, image)
        yval.append(mean((array(imread(imageLocation, 0))).flatten()))
        xval.append(int(image[5:-4]))

    xval = array(xval)
    yval = array(yval)
    numKeyFrames = round(len(yval) * percentKeyFrames)

    while True:
        indices = argrelmax(yval)[0]  # local maxima
        if len(indices) <= numKeyFrames:
            xval = deepcopy(xval[indices])
            break
        yval = deepcopy(yval[indices])
        xval = deepcopy(xval[indices])

    xval = set(xval)
    xval.add(0)
    xval.add(len(images) - 1)

    print("Total Number of frames : ", len(images), "\n",
          "Key Frames Identified : ", len(xval))

    try:
        # creating a folder
        if path.exists(newFolderName):
            rmtree(path.join(workingDirectory, newFolderName))
        makedirs(newFolderName)
    # if not created then raise error
    except OSError:
        raise Exception("Error: Creating directory of KeyFrames")

    for index in xval:
        image = f"frame{index}.jpg"
        src = path.join(workingDirectory, imageFolderName, image)
        dest = path.join(workingDirectory, newFolderName, image)
        copy(src, dest)
