import os
from shutil import rmtree

from cv2 import imread, imwrite
from face_recognition.api import batch_face_locations


def function(workingDirectory, imageFolderName, newFolderName):
    # offset = 50
    offset = 20
    try:
        # creating a folder
        if os.path.exists(newFolderName):
            rmtree(os.path.join(workingDirectory, newFolderName))
        os.makedirs(newFolderName)
    # if not created then raise error
    except OSError:
        raise Exception("Error: Creating directory of Extracted Faces")

    image_arrays = [
        imread(os.path.join(
            workingDirectory, imageFolderName, image))
        for image in os.listdir(os.path.join(
            workingDirectory, imageFolderName))]
    image_names = [image_name for image_name in os.listdir(os.path.join(
        workingDirectory, imageFolderName))]

    face_locations = batch_face_locations(
        images=image_arrays, number_of_times_to_upsample=0, batch_size=8)

    name_array_dict = {name: array for name,
                       array in zip(image_names, image_arrays)}

    for name, array in zip(image_names, face_locations):
        try:
            if len(array) == 1:
                top, right, bottom, left = array[0]
                face_image = name_array_dict[name][top -
                                                   offset: bottom + offset, left - offset: right + offset]
                path = os.path.join(
                    workingDirectory, newFolderName, f"{name[:-4]}_{0}.jpg")
                imwrite(path, face_image)
            elif len(array) > 1:
                face_count = 0
                for face_location in array:
                    top, right, bottom, left = face_location
                    face_image = name_array_dict[name][top:bottom, left:right]
                    path = os.path.join(
                        workingDirectory, newFolderName, f"{name[:-4]}_{face_count}.jpg")
                    imwrite(path, face_image)
                    face_count += 1
        except:
            print(f"The image {name} could not be read properly")
