import csv
import os
import progressbar

performSets = ["validation", "test", "train"]
for performSet in performSets:
    data = performSet + ".csv"
    images_folder = performSet + "_resized/"
    images = []

    with open(data, 'rb') as f:
        reader = csv.reader(f)
        data = list(reader)

    data = data[1:]

    images = os.listdir(images_folder)

    def getRowContaining(image):
        for row in data:
            if image == row[0]:
                return row

    pbar = progressbar.ProgressBar()
    for image in pbar(images):
        if "ISIC" in image:
            row = getRowContaining(image.split(".")[0])
            if row[1] == "1.0":
                os.rename(images_folder + image,
                          images_folder + "pos/" + image)
            else:
                os.rename(images_folder + image,
                          images_folder + "neg/" + image)
