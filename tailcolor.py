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
        #print fade
        r = 255 + fade
        g = min((self.age()*scaler), 255) + fade
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
    import os
    import blessings

    f = subprocess.Popen(['tail','-F',sys.argv[1]],\
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    lines = ['-']
    print ""
    term = blessings.Terminal()

    try:
        os.system('setterm -cursor off')
        while True:
            #print 'main'
            ready = p.poll(1)
            line = ''
            #print ready
            if ready:
                if ready[0][1] == select.POLLHUP:
                    #print 'POLLHUP'
                    break
                if ready[0][1] == select.POLLIN:
                    while ready[0][1] & select.POLLIN:
                        #print 'poll1', ready,len(lines)
                        #if len(lines) > 44440:
                        #    _ = lines.pop(0)
                        char = f.stdout.read(1)
                        line += char
                        #print line
                        if char == '\n': 
                            if len(lines)>term.height-1: lines.pop(0)
                            lines.append(heatmap(line,1))
                            line = ''
                            break
                    #lines.append(tailcolor.heatmap(f.stdout.read(1), scale=20))
            else:
                pass
		#print 'poll0'
                #time.sleep(0.1)
            #print 'clearing screen'
            time.sleep(0.1)
            #if len(lines) < 30: print "\n" * 30 
            #print 'printing lines'
            #print len(lines)
            for x in range(term.height-1):
                with term.location(0, x): 
                    #      if len(lines)>18: time.sleep(0.5)
                    try:
                       # print x,
                        if x < len(lines):
                            print str(lines[x+1]).replace('\n','') + term.clear_eol
                      #      time.sleep(0.1)
                        else:
            #                print x,
             #               time.sleep(0.1)
                            print term.clear_eol
                    except IndexError:
                        print term.clear_eol
            #sys.stdout.flush()
    except KeyboardInterrupt:
        os.system('setterm -cursor on')
