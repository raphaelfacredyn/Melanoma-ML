import csv #load csv
import os #change directory as needed and create new folders
import shutil #load files into a new folder

os.chdir('C:\\Users\\rneervannan\\Desktop\\siemens-science-fair\\Melanoma-data') #change directory to the folder with images
id_dict = {}
file_names = []
# id_dict contains image id/classification pairs in the form of key/value pairs
# file_names contains the names of files with melanoma
with open('validation.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        id_dict[row[0]] = row[1]
del id_dict['image_id']
# load the .csv file into a dictionary and delete the header row ('image_id': 'melanoma')
for key, value in id_dict.iteritems():
    value = float(value)
    if value == 1.0:
        file_names.append(key)
#create a list that has all of the image ids with melanoma
os.mkdir('melanoma-validation')
os.chdir('C:\\Users\\rneervannan\\Desktop\\siemens-science-fair\\Melanoma-data\\Validation')
#create a new directory for the images with melanoma and change the directory to the folder with all scans
for file in file_names:
    shutil.move(file+".jpg", 'C:\\Users\\rneervannan\\Desktop\\siemens-science-fair\\Melanoma-data\\melanoma-validation')
#move all files with melanoma to a different folder