import csv

with open('player-complete.csv', 'rb') as allUsernames:
    reader1 = csv.reader(allUsernames, delimiter=',')
    for row in reader1: 
        print(row)
        # with open('usernames.csv', 'rb') as usersAndHandles:
        #     reader2 = csv.reader(usersAndHandles, delimiter=',')
        #     for row in uReader:
        #         print(row[1] == '')