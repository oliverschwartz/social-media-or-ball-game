import sys

chars = set('0123456789')
def isNum(char):
    if any((c in chars) for c in char):
        return True
    else: return False

for line in sys.stdin:
    for i in range(0, len(line)):
        if isNum(line[i]): 
            sys.stdout.write(line[:i] + ',' + line[i:])
            break
