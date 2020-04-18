import pygame
import pygame.gfxdraw
import math

from calculation import *
from drawing import *

class Visual:
    def draw(self, screen):
        pass

class VectorVisual(Visual):
    def __init__(self, origin, xy, color, arrow_w, arrow_h, width = 1):
        self.origin = origin
        self.xy = xy
        self.color = color
        self.arrow_w = arrow_w
        self.arrow_h = arrow_h
        self.width = width
        
    def draw(self, screen):
        # Tail
        lenxy = lenv(self.xy)
        if lenxy == 0:
            lenxy = 1
        end = addvecs(self.origin, scalevec(1 - self.arrow_h / lenxy, self.xy))
        pygame.draw.line(screen, self.color, self.origin, end, self.width)
        # Arrow
        end = addvecs(self.origin, self.xy)
        arrow_w2 = self.arrow_w / 2
        xaxis = norm(self.xy)
        yaxis = rotate90cc(xaxis)
        nyaxis = rotate90c(xaxis)
        arrow1end = addvecs(end, addvecs(scalevec(-self.arrow_h, xaxis), scalevec(arrow_w2, yaxis)))
        arrow2end = addvecs(end, addvecs(scalevec(-self.arrow_h, xaxis), scalevec(arrow_w2, nyaxis)))
        pygame.draw.polygon(screen, self.color, [end, arrow1end, arrow2end])
        
class SegmentVisual(Visual):
    def __init__(self, start, end, color, width = 1, text = "", font = None, fontcolor = (0, 0, 0), font_highlight = None):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        self.text = text
        self.font = font
        self.fontcolor = fontcolor
        self.font_highlight = font_highlight
        
    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.start, self.end, self.width)
        vec = subvecs(self.end, self.start)
        lenseg = lenv(vec)
        if lenseg == 0:
            lenseg = 1
        if self.font is not None:
            (tw, th) = textsize = self.font.size(self.text)
            if lenseg >= tw and lenseg >= th:
                drawpos = addvecs(self.start, scalevec(0.5, subvecs(vec, textsize)))
                screen.blit(pygame.transform.flip(self.font.render(self.text, True, self.fontcolor, self.font_highlight), False, True), drawpos)
        
        
class AngleVisual(Visual):
    def __init__(self, pt, v0, v1, r, color, fillcolor = None, width = 1):
        self.pt = pt
        self.r = r
        self.color = color
        self.fillcolor = fillcolor
        self.width = width
        self.v0 = v0
        self.v1 = v1
        angle0 = angle(v0)
        angle1 = angle(v1)
        self.anglediff = (angle1 - angle0) % math.tau
        if self.anglediff > math.pi:
            t = angle0
            angle0 = angle1
            angle1 = t
            self.anglediff = math.tau - self.anglediff
        self.startangle = angle0
        self.endangle = angle1
        
    def draw(self, screen):
        shrink = 1.5 * (self.anglediff if self.anglediff > 0 else 1)
        actual_r = min(max(self.r / shrink, self.r), lenv(self.v0) / 2, lenv(self.v1) / 2)
        if actual_r > self.width:
            # Do acute or obtuse angle
            if not (abs(self.anglediff - math.pi / 2) < 0.001):
                if self.fillcolor is not None:
                    inner_r = actual_r - self.width
                    do_arc(screen, self.fillcolor, self.pt, inner_r, self.startangle, self.endangle, inner_r)
                do_arc(screen, self.color, self.pt, actual_r, self.startangle, self.endangle, self.width)
            # Do right angle
            else:
                slen = actual_r / math.sqrt(2)
                v0n = norm(self.v0)
                v1n = norm(self.v1)
                p0 = addvecs(self.pt, scalevec(slen, v0n))
                p2 = addvecs(self.pt, scalevec(slen, v1n))
                p1 = addvecs(p0, scalevec(slen, v1n))
                if self.fillcolor is not None:
                    pygame.draw.polygon(screen, self.fillcolor, [p0, p1, p2, self.pt])
                pygame.draw.line(screen, self.color, p0, p1, self.width)
                pygame.draw.line(screen, self.color, p1, p2, self.width)
                
class AreaVisual(Visual):
    def __init__(self, color, pts):
        self.color = color
        self.pts = pts
        
    def draw(self, screen):
        if len(self.pts) >= 3:
            pygame.draw.polygon(screen, self.color, self.pts)

class TextVisual(Visual):
    def __init__(self, pos, text, font, fontcolor = (0, 0, 0), font_highlight = None):
        self.pos = pos
        self.text = text
        self.font = font
        self.fontcolor = fontcolor
        self.font_highlight = font_highlight
        
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.font.render(self.text, True, self.fontcolor, self.font_highlight), False, True), self.pos)
        