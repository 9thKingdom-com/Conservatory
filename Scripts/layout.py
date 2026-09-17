"""Shared deterministic site coordinates, in metres. Unreal conversion is at the boundary."""
import math
SEED=5802
def height(x,y):
    h=7+55*math.exp(-((x+170)/180)**2-(y/230)**2)
    h+=14*math.exp(-((x+390)/150)**2-((y-180)/160)**2)
    h+=44*math.exp(-((x-340)/220)**2-((y-460)/140)**2)
    h+=32*math.exp(-((x+100)/240)**2-((y+490)/130)**2)
    h+=2.2*math.sin(x*.022)*math.sin(y*.017)+.65*math.sin(x*.073+y*.039)
    d=max(abs(x+175)/52,abs(y)/40)
    t=max(0,min(1,(d-1)/.65)); t=t*t*(3-2*t)
    return 62*(1-t)+h*t
def path_y(x):
    return -37-31*math.sin((x+130)/85)
def clearing(x,y,margin=0):
    return abs(x+175)<55+margin and abs(y)<43+margin
def village(x,y):
    return 130<x<310 and -100<y<110
