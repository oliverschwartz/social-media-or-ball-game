from __future__ import print_function
import csv

with open('players-complete.csv', 'rb') as allUsernames:
    reader1 = csv.reader(allUsernames, delimiter=',')
    for row1 in reader1:
        found = False
        with open('usernames.csv', 'rb') as usersAndHandles:
            reader2 = csv.reader(usersAndHandles, delimiter=',')
            for row2 in reader2:
                if (row1[0] == row2[0]):
                    found = True
                    print(row1[0] + ",", end='')
                    if (row2[1] != ''): print(row2[1])
                    else: print()
            if not found:
                print(row1[0] + ",")
            