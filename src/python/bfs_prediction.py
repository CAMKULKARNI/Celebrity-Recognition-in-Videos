from os import listdir, path

from cv2 import IMREAD_UNCHANGED, INTER_AREA, imread, resize
# from face_recognition import face_encodings
from deepface.DeepFace import verify
from tensorflow import reduce_sum, square, subtract


def prediction(img1, img2):
    try:
        # img1 = face_encodings(img1)[0]
        # img2 = face_encodings(img2)[0]
        # dist = reduce_sum(square(subtract(img1, img2)), -1)
        # return float(dist)
       result = verify(img1, img2, detector_backend="retinaface", model_name="VGG-Face")
       return result["verified"]
    except Exception as e:
        print("Error in prediction: ", e)
        return None


def function(workingDirectory, imageFolderName, reference_images):
    numberimgsperclass = 10
    dim = (200, 200)
    results = []
    test = path.join(workingDirectory, imageFolderName)
    test_images = listdir(test)

    references = listdir(path.join(workingDirectory, reference_images))
    queue = dict()
    for celeb in references:
        queue[celeb] = [
            listdir(path.join(path.join(workingDirectory, reference_images, celeb))), 0]

    imagec = 0

    for image in test_images:
        imagec += 1
        img1 = path.join(workingDirectory, imageFolderName, image)
        # img1 = imread(img1, IMREAD_UNCHANGED)
        # img1 = resize(img1, dim, interpolation=INTER_AREA)

        for celeb in queue:
            queue[celeb][1] = 0
        flag = False
        if len(queue) == 0:
            return results
        for i in range(numberimgsperclass):
            for celebs in queue:
                if queue[celebs][1] >= 3:
                    j = queue[celebs][1]
                    while j < numberimgsperclass:
                        if queue[celebs][1] >= 6:
                            results.append(celebs)
                            del queue[celebs]
                            flag = True
                            break
                        img2 = path.join(
                            workingDirectory, reference_images, celebs, queue[celebs][0][j])
                        # img2 = imread(img2, IMREAD_UNCHANGED)
                        # img2 = resize(img2, dim, interpolation=INTER_AREA)
                        # distance = prediction(img1, img2)
                        # if distance != None and distance < 0.4:
                        #     queue[celebs][1] += 1
                        verified = prediction(img1, img2)
                        if verified:
                            queue[celebs][1] += 1
                        j += 1
                else:
                    img2 = path.join(
                        workingDirectory, reference_images, celebs, queue[celebs][0][i])
                    # img2 = imread(img2, IMREAD_UNCHANGED)
                    # img2 = resize(img2, dim, interpolation=INTER_AREA)
                    # distance = prediction(img1, img2)
                    # if distance != None and distance < 0.4:
                    #     queue[celebs][1] += 1
                    verified = prediction(img1, img2)
                    if verified:
                        queue[celebs][1] += 1
                if flag == True:
                    break

            if flag == True:
                break

    return results
