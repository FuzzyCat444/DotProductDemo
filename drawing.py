import pygame
import math

def do_arc(screen, color, xy, r, startangle, endangle, width = 1):
    anglediff = endangle - startangle
    if anglediff < 0.001:
        return
    (x, y) = xy
    inner_r = r - width
    startangle %= math.tau
    endangle %= math.tau
    if endangle < startangle:
        endangle += math.tau
    degs = math.degrees(anglediff)
    arc = []
    innerarc = []
    radangle = startangle
    degstep = 1
    frac = degs % degstep
    angleincr = math.radians(degstep)
    
    def putpoints():
        cos = math.cos(radangle)
        sin = math.sin(radangle)
        arc.append((x + r * cos, y + r * sin))
        innerarc.append((x + inner_r * cos, y + inner_r * sin))
    
    putpoints()
    while degs >= degstep:
        radangle += angleincr
        degs -= degstep
        putpoints()
    radangle += math.radians(frac)
    putpoints()
    
    polygon = arc + list(reversed(innerarc))
    if len(polygon) >= 3:
        pygame.draw.polygon(screen, color, polygon)