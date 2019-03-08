import glob
import csv

path = "*.csv"

for fname in glob.glob(path):
    with open(fname, "rb") as file:
        reader = csv.reader(file)
        firstLine = True
        for line in reader:
            if firstLine:
                firstLine = False
            else:
                print(line[1])