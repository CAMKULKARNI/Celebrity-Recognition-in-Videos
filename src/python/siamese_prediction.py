from os import listdir, path

from cv2 import IMREAD_UNCHANGED, INTER_AREA, imread, resize
from face_recognition import face_encodings
from tensorflow import reduce_sum, square, subtract


def prediction(img1, img2):
    dim = (200, 200)
    img1 = imread(img1, IMREAD_UNCHANGED)
    img1 = resize(img1, dim, interpolation=INTER_AREA)
    img2 = imread(img2, IMREAD_UNCHANGED)
    img2 = resize(img2, dim, interpolation=INTER_AREA)

    try:
        img1 = face_encodings(img1)[0]
        img2 = face_encodings(img2)[0]
        dist = reduce_sum(square(subtract(img1, img2)), -1)

        return float(dist)

    except:
        return None


def function(workingDirectory, imageFolderName, reference_images):
    results = set()
    test = path.join(workingDirectory, imageFolderName)
    test_images = listdir(test)

    references = listdir(path.join(workingDirectory, reference_images))

    for image in test_images:
        for celeb in references:
            celeb_images = listdir(path.join(
                path.join(workingDirectory, reference_images, celeb)))
            count = 0
            for celeb_image in celeb_images:
                image1 = path.join(workingDirectory, imageFolderName, image)
                image2 = path.join(
                    workingDirectory, reference_images, celeb, celeb_image)
                distance = prediction(image1, image2)
                if distance != None and distance < 0.4:
                    count += 1

            if count >= 12:
                results.add(celeb)

    print(results)
    return list(results)
