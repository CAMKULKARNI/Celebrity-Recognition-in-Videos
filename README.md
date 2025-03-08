# Celebrity Recognition in Videos

This project recognises celebrities in a given video using deep learning techniques. It leverages pre-trained models and custom code to identify and track celebrities within video footage.

## Project Structure

The project is organized as follows:

*   `105_classes_pin_dataset/`: A directory of 105 sub-directories containing an average of about 200 images of 105 celebrities. This dataset is used at runtime to determine which celebrity's face is currently in the frame. The dataset can be extracted using dataset/archieve.zip
*   `src/python/`: Contains the python source code for the project.
    * The entire project is written in Python 3.x.
    *   `bfs_prediction.py`: This file implements a function for the celebrity recognition logic. It takes the paths to the test image folder and the reference images folder as input. It iterates through the test images, compares them against the reference images, and returns a list of predicted celebrities.
    *   `faceExtraction.py`: This file implements a function that takes the working directory, the name of the folder containing the images, and the name of the folder where the extracted faces will be saved as input. It detects faces in each image and saves the extracted faces as individual .jpg files in the new folder.
    *   `siamese_prediction.py`: This file implements a function that takes the paths to two images as input, reads the images, resizes them, generates face encodings using the face_recognition library, and returns the Euclidean distance between the encodings using TensorFlow.
    *   `video_processing.py`: This file implements a function that takes the working directory, the name of the folder containing the images, the name of the folder where the extracted key frames will be saved, and the desired percentage of key frames as input. It calculates the mean pixel intensity for each frame, identifies local maxima, selects a subset of frames as key frames, and saves them to the new folder.
*   `videoToImage.py`: This file has functions to extract frames from a given video and put them in a directory given.

## Dependencies

The project requires the following libraries:

*   `opencv-python`
*   `numpy`
*   `scikit-learn`
*   `tensorflow`
*   `dlib`
*   `face_recognition`


## Usage

Currently there are some issues that are being faced while installing the dlib dependencies on a local machine. But if the user is successfully able to install all the dependencies, executing the following command would you give the list of celebrities.

```bash
python src/video_processing.py --input_video path/to/your/video.mp4 --output_video path/to/output/video.mp4
```

Else the project is hosted on Github and can be connected to colab and executing the given Jupyter Notebook line-by-line would give the same result.

A small demo of the project can also be seen in [Demo.mp4](Demo.mp4)