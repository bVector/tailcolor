#!/usr/bin/env python
import fabulous
from fabulous.color import *
import time

class heatmap():
    def __init__(self, text, scale=1):
        self.text = text
        self.time = int(time.time()*5)
        self.scale = scale

    def age(self):
        return (int(time.time()*5) - self.time)

    def redfade(self, scale=None):
        if scale:
            scaler = scale
        else:
            scaler = self.scale
        fade = max(min(200 - self.age()*scaler,0),-120)
        r = 255 + fade
        g = min((self.age()*scaler), 255) + fade
        b = g
        color = '#{0:02x}{1:02x}{2:02x}'.format(r,g,b)
        return color

    def __str__(self):
        return str(fg256(self.redfade(), self.text))

if __name__ == '__main__':
    import subprocess, select
    import sys, os, time
    import blessings

    f = subprocess.Popen(
    	['tail','-F',sys.argv[1]],
    	stdout=subprocess.PIPE,
    	stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    lines = ['-']
    print ""
    delay = 0.01
    term = blessings.Terminal()

    try:
        os.system('setterm -cursor off')
        while True:
            ready = p.poll(1)
            line = ''
            if ready:
                if ready[0][1] == select.POLLHUP:
                    break
                if ready[0][1] == select.POLLIN:
                    while ready[0][1] & select.POLLIN:
                        char = f.stdout.read(1)
                        line += char
                        if char == '\n': 
                            if len(lines)>term.height-1: lines.pop(0)
                            lines.append(heatmap(line,1))
                            delay = 0
                            line = ''
                            break
            time.sleep(delay)
            delay = min(delay + 0.01, 1)
            for x in range(term.height-1):
                with term.location(0, x): 
                    try:
                        if x < len(lines):
                            print str(lines[x+1]).replace('\n','') + term.clear_eol
                        else:
                            print term.clear_eol
                    except IndexError:
                        print term.clear_eol
    except KeyboardInterrupt:
        os.system('setterm -cursor on')
