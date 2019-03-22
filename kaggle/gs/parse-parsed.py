import os, csv, sys, operator

os.chdir('pages')

for file in os.listdir():
    gs = []
    players = []

    # Sort through the parsed html
    if file[-6:] == "parsed":
        with open(file, 'r') as inp:
            reader = csv.reader(inp)
            foundStats = False
            writeName = True
            for line in reader:
                if not foundStats:
                    if line[0].replace('.','',1).isdigit():
                        foundStats = True
                    elif writeName:
                        players.append(line)
                        writeName = False
                    else:
                        writeName = True
                if foundStats:
                    gs.append(line[0])
        
        sys.stdout = open(file[:2] + "-gs.csv", 'a')
        
        # Check that number of GS stats matches number of players
        if len(gs) != len(players):
            print("broken!")
            print(file)
            print(len(players))
            print(len(gs))
            sys.exit(1)
        else:
            for i in range(0, len(gs)):
                print(players[i][1].strip() + ",", end='')
                print(players[i][0].strip() + ",", end='')
                print(gs[i])
