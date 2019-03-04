import sys
prevLine = ''
for line in sys.stdin:
    if line != prevLine:
        sys.stdout.write(line)
    prevLine = line