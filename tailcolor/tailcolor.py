#!/usr/bin/env python
import blessings, fabulous
from fabulous.color import *
import time, os, itertools
from sarge import run, Capture
from math import sin, pi

class HeatmapTerminal(object):
    def __init__(self, pattern='redfade'):
        self.term = blessings.Terminal()
        self.lines = []
        self.pattern = pattern

    def addline(self, linetext, scale=1):
        linetext = linetext.replace('\n','')
        linetext = linetext.replace('\t',' '*8)
        for line in self.breaktext(linetext):
            self.lines.append(Heatmap(line, scale=scale, pattern=self.pattern))
            self.trimlines()
            self.draw()
  
    def trimlines(self):
        while len(self.lines) >= self.term.height:
            topline = self.lines.pop(0)
            with self.term.location(0,0):
                print topline.text,
            with self.term.location(0,self.term.height-1):
                print ''

    def breaktext(self,linetext):
        while len(linetext):
            snip = min(self.term.width, len(linetext))
            linetext, line = linetext[snip:], linetext[:snip]
            yield line

    def draw(self,exit=False):
        for text, height in itertools.izip_longest(
                reversed(self.lines),
                reversed(range(self.term.height-1)),
                fillvalue = None):          
            with self.term.location(-1,height):
                if isinstance(text, Heatmap):
                    if exit:
                        print self.term.clear_bol + text.text
                    else:
                        print self.term.clear_bol + str(text) + self.term.clear_eol


class Heatmap(object):
    def __init__(self, text, scale=1, pattern='redfade'):
        self.text = text
        self.color = getattr(self, pattern)
        self.time = int(time.time()*5)
        self.scale = scale

    def age(self):
        return (int(time.time()*5) - self.time)

    def flashing(self):
        if self.age() < 25:
            timer = time.time()
            g = int((timer - int(timer))*254)            
        else:
            return(180,180,180)
        b = g
        r = 255
        return (r,g,b)

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

    def rainbowfade(self, scale=0.3):
        if scale:
            scaler = scale
        else:
            scaler = self.scale
        fade = min(max(self.age()*scaler,0),4*pi)
        percent = fade / (4*pi)
        r = int(sin(fade*1.25+1.25) * 255 + 0)
        g = int(sin(fade*1.25+6.0) * 255 + 0)
        b = int(sin(fade*1.25+4.0) * 255 + 0)
        r = int((r * (1-percent) + 200 * percent))
        g = int((g * (1-percent) + 200 * percent))
        b = int((b * (1-percent) + 200 * percent))
        r,g,b = [min(max(_,0),255) for _ in [r,g,b]]
        return (r, g, b)

    def __str__(self):
        color = self.color()
        return str(fg256(color, (self.text)))

def runloop(pattern='redfade'):
    try:
        os.system('setterm -cursor off')
        #os.system('stty -echo')
        term = HeatmapTerminal(pattern=pattern)
        delay = 0
        p = run('cat', input=sys.stdin, async=True, stdout=Capture(buffer_size=1), stderr=Capture())
        print term.term.move(100,0),
        while True:
            line = p.stdout.readline()
            if line: 
                term.addline(line)
                delay = 0
            term.draw()
            time.sleep(delay)
            delay = min(delay + 0.01, 0.25)
    except KeyboardInterrupt:
        term.draw(exit=True)
        #print term.term.move(term.term.width, term.term.height),
    finally:
        os.system('setterm -cursor on')
        #os.system('stty echo')
        p.wait()
        p.close()

if __name__ == '__main__':
    runloop()
