from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from os import makedirs, path
from shutil import rmtree

from cv2 import CAP_PROP_FRAME_COUNT, VideoCapture, imwrite


def extract_frames(video_path, newImageFolder, start=-1, end=-1):
    """
    Extract frames from a video using OpenCVs VideoCapture
    :param video_path: path of the video
    :param newImageFolder: the directory to save the frames
    :param start: start frame
    :param end: end frame
    :param every: frame spacing
    :return: count of images saved
    """

    # make the paths OS (Windows) compatible
    video_path = path.normpath(video_path)
    # make the paths OS (Windows) compatible
    newImageFolder = path.normpath(newImageFolder)

    assert path.exists(video_path)  # assert the video file exists

    capture = VideoCapture(video_path)  # open the video using OpenCV

    if start < 0:  # if start isn't specified lets assume 0
        start = 0
    if end < 0:  # if end isn't specified assume the end of the video
        end = int(capture.get(CAP_PROP_FRAME_COUNT))

    capture.set(1, start)  # set the starting frame of the capture
    frame = start  # keep track of which frame we are up to, starting from start
    # a safety counter to ensure we don't enter an infinite while loop (hopefully we won't need it)

    while frame < end:  # lets loop through the frames until the end

        _, image = capture.read()  # read an image from the capture

        save_path = path.join(newImageFolder, f"frame{frame}.jpg")
        # if it doesn't exist
        if not path.exists(save_path):
            imwrite(save_path, image)  # save the extracted image

        frame += 1  # increment our frame count

    capture.release()  # after the while has finished close the capture


def function(workingDirectory, video_path, newImageFolder, chunk_size=1000):
    """
    Extracts the frames from a video using multiprocessing
    :param video_path: path to the video
    :param newImageFolder: directory to save the frames
    :param every: extract every this many frames
    :param chunk_size: how many frames to split into chunks (one chunk per cpu core process)
    :return: path to the directory where the frames were saved, or None if fails
    """

    # make the paths OS (Windows) compatible
    # path.join(workingDirectory, video + ".mp4")
    video_path = path.normpath(video_path)
    # make the paths OS (Windows) compatible
    newImageFolder = path.normpath(newImageFolder)

    # make directory to save frames, its a sub dir in the newImageFolder with the video name
    try:
        # creating a folder
        if path.exists(newImageFolder):
            rmtree(path.join(workingDirectory, newImageFolder))
        makedirs(newImageFolder)
    # if not created then raise error
    except OSError:
        raise Exception("Error: Creating directory of Frames")

    capture = VideoCapture(video_path)  # load the video
    # get its total frame count
    total = int(capture.get(CAP_PROP_FRAME_COUNT))
    capture.release()  # release the capture straight away

    if total < 1:  # if video has no frames, might be and opencv error
        print("Video has no frames. Check your OpenCV + ffmpeg installation")
        return None  # return None

    # split the frames into chunk lists
    frame_chunks = [[i, i+chunk_size] for i in range(0, total, chunk_size)]
    # make sure last chunk has correct end frame, also handles case chunk_size < total
    frame_chunks[-1][-1] = min(frame_chunks[-1][-1], total-1)

    # execute across multiple cpu cores to speed up processing, get the count automatically
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        for f in frame_chunks:
            # submit the processes: extract_frames(...)
            executor.submit(extract_frames, video_path,
                            newImageFolder, f[0], f[1])
