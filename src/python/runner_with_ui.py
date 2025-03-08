from os import getcwd, path
from time import sleep, time
from tkinter import Button, Label, Text, Tk, ttk
from tkinter.constants import HORIZONTAL, INSERT, WORD

from PIL import Image, ImageTk

from bfs_prediction import function as F_R
from faceExtraction import function as F_E
from video_processing import function as V_P
from videoToImage import function as VTI

index = 0
video_name = ""
percentKeyFrames = 0.1
results = []


def clickedPrev(celebs):
    global index
    if index > -1:
        img = ImageTk.PhotoImage(Image.open(
            f'{path.join(getcwd(), "Celebrities", "Images", celebs[index])}.jfif').resize((1000, 750)))
        info = Text(window, width=63, height=750,
                    bg="orange", wrap=WORD)
        info.place(x=1015, y=10)
        data = ""
        with open(f'{path.join(getcwd(), "Celebrities", "Info", celebs[index])}.txt', 'r') as file:
            data = file.read().replace('\n', '')
        info.insert(INSERT, data)
        index -= 1
        panel = Label(window, image=img)
        panel.image = img
        panel.place(x=10, y=10)
    if index < 0:
        index = 0


def clickedNext(celebs):
    global index
    if index < len(celebs):
        img = ImageTk.PhotoImage(Image.open(
            f'{path.join(getcwd(), "Celebrities", "Images", celebs[index])}.jfif').resize((1000, 750)))
        info = Text(window, width=63, height=750,
                    bg="orange", wrap=WORD)
        info.place(x=1015, y=10)
        data = ""
        with open(f'{path.join(getcwd(), "Celebrities", "Info", celebs[index])}.txt', 'r') as file:
            data = file.read().replace('\n', '')
        info.insert(INSERT, data)
        index += 1
        panel = Label(window, image=img)
        panel.image = img
        panel.place(x=10, y=10)
    if index > len(celebs) - 1:
        index = len(celebs) - 1


def getVideoName():
    global video_name
    global percentKeyFrames
    video_name = videoName.get(1.0, "end-1c")
    percentKeyFrames = float(keyFramePercentage.get(1.0, "end-1c")) / 100
    start = time()
    execute()
    print(f"Took {time() - start}")


def updateProgressBar(value, function):
    progress['value'] = value
    window.update()
    sleep(1)


def takeResults(workingDirectory):
    global results
    results = F_R(workingDirectory=workingDirectory,
                  imageFolderName="Faces", reference_images="new dataset")


def execute():
    updateProgressBar(value=25, function=VTI(workingDirectory=workingDirectory,
                      video_path=f'{path.join(workingDirectory, video_name) + ".mp4"}', newImageFolder="data", chunk_size=350))
    updateProgressBar(value=50, function=V_P(workingDirectory=workingDirectory,
                      imageFolderName="data", newFolderName="Key Frames", percentKeyFrames=percentKeyFrames))
    updateProgressBar(value=75, function=F_E(
        workingDirectory=workingDirectory, imageFolderName="Key Frames", newFolderName="Faces"))
    updateProgressBar(value=100, function=takeResults(
        workingDirectory=workingDirectory))


if __name__ == "__main__":
    workingDirectory = getcwd()
    window = Tk()

    window.title("Celebrity Recognition in Videos")
    window.geometry('1960x1080')
    window.configure(background='black')

    videoName = Text(window, height=1, width=20)
    videoName.place(x=10, y=10)
    keyFramePercentage = Text(window, height=1, width=20)
    keyFramePercentage.place(x=200, y=10)

    go = Button(window, text="GO!!!", command=getVideoName)
    go.place(x=20, y=40)

    progress = ttk.Progressbar(
        window, orient=HORIZONTAL, length=1000, mode='determinate')
    progress.place(x=200, y=200)

    prev = Button(
        window, text="Previous", command=lambda: clickedPrev(results))
    prev.place(x=110, y=780)
    next = Button(
        window, text="Next", command=lambda: clickedNext(results))
    next.place(x=320, y=780)

    window.mainloop()
