import os, sys, csv, shutil

# check python2.7 being used
if sys.version_info >= (3, 0):
    print("use Python 2.7, not 3!")
    sys.exit()

os.chdir('../')

# parse each csv in ig/playerFollowing
for file in os.listdir('.'):
    # check if file is a csv
    if file[-4:] == '.csv':
        with open(file[:-4] + "_processed.csv", "w") as fw:
            with open(file, 'rU') as fr:
                reader = csv.reader(fr)
                readFirst = False
                for line in reader:
                    if readFirst:
                        fw.write(line[1] + "\n")
                    else:
                        readFirst = True

print("now, run: \"cd ..; mv *_processed.csv processed\"")