import csv

with open("new.csv", "w") as w:
	with open("playervotes17.csv", "r") as r:
		reader = csv.reader(r, delimiter=',')
		for line in reader:
			w.write(line[0] + ",")
			if line[4] == '':
				w.write("0\n")
			else:
				w.write(line[4] + "\n")