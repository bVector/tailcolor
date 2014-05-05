#!/usr/bin/env python
import fabulous
from fabulous.color import *
import time

class heatmap():
    def __init__(self, text, scale=1):
        self.text = text
        self.time = int(time.time())
        self.scale = scale

    def age(self):
        return (int(time.time()) - self.time)

    def redfade(self, scale=None):
        if scale:
            scaler = scale
        else:
            scaler = self.scale
        r = 255
        g = min((self.age()*scaler), 255)
        b = g
        color = '#{0:02x}{1:02x}{2:02x}'.format(r,g,b)
        return color

    def __str__(self):
        return str(fg256(self.redfade(), self.text))

#if __name__ == '__main__':
#    import fileinput, time, sys
#    lines = [heatmap('-') for x in range(10)]
#    pipe = fileinput.input()
#    while True:
#        piped = sys.stdin.readline()
#        if piped:
#            _ = lines.pop(0)
#            lines.append(heatmap(piped))
#        else:
#            time.sleep(1)
#            print "\n" * 60
#            for line in lines:
#                #print line.redfade, line.text
#                print fg256(line.redfade(), line.text),

if __name__ == '__main__':
    import time
    import subprocess
    import select
    import tailcolor
    import sys

    f = subprocess.Popen(['tail','-F',sys.argv[1]],\
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    lines = []
    print ""

    try:
        while True:
            if p.poll(1):
                if len(lines) > 60:
                    _ = lines.pop(0)
                lines.append(tailcolor.heatmap(f.stdout.readline()))
            else:
                time.sleep(1)
            print "\n" * 60
            for line in lines:
                print line,
    except KeyboardInterrupt:
        pass
