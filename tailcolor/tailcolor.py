#!/usr/bin/env python
import blessings, fabulous
from fabulous.color import *
import time, os, itertools
from sarge import run, Capture

class HeatmapTerminal(object):
    def __init__(self):
        self.term = blessings.Terminal()
        self.lines = []

    def addline(self, linetext, scale=1):
        linetext = linetext.replace('\n','')
        linetext = linetext.replace('\t',' '*8)
        self.lines.append(Heatmap(linetext, scale=scale))
        with self.term.location(self.term.width, self.term.height):
            print ''
        while len(self.lines) >= self.term.height:
            _ = self.lines.pop(0)

    def draw(self):
#        with self.term.location(self.term.width,self.term.height):
#            print ''
        for text, height in itertools.izip_longest(
                reversed(self.lines),
                reversed(range(self.term.height-1)),
                fillvalue = -1):
#            with self.term.location(0,height):
#                if text: 
#                    print self.term.clear_eol + '>printing {0} on line {1}'.format(text, height),
#                    time.sleep(1.25)
            with self.term.location(-1,height):
                if text != -1:
                    if height == 0:
                        print self.term.clear_bol + text.text
                    else:
                        print self.term.clear_bol + str(text) + self.term.clear_eol

class Heatmap(object):
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

def runloop():
    try:
        os.system('setterm -cursor off')
        term = HeatmapTerminal()
        p = run('cat', input=sys.stdin, async=True, stdout=Capture(buffer_size=1), stderr=Capture())
        while True:
            line = p.stdout.readline()
            if line: term.addline(line)
            term.draw()
            time.sleep(0.01)
    except KeyboardInterrupt:
        term.term.move(term.term.width, term.term.height)
        print 'end'
    finally:
        os.system('setterm -cursor on')
        p.wait()
        p.close()

if __name__ == '__main__':
    runloop()
