import pygame
import math

class DraggablePoint:
    def __init__(self, r, xy = (0,0)):
        self.r2 = r * r
        self.xy = xy
        self.dragging = False
        
    def event(self, event, mousepos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.startdrag(mousepos)
        elif event.type == pygame.MOUSEBUTTONUP:
            return self.enddrag(mousepos)
        elif event.type == pygame.MOUSEMOTION:
            return self.drag(mousepos)
            
    def startdrag(self, mousepos):
        (mx, my) = mousepos
        (x, y) = self.xy
        if (x - mx) ** 2 + (y - my) ** 2 < self.r2:
            self.dragging = True
            self.xy = mousepos
            return True
        return False
        
    def enddrag(self, mousepos):
        if (self.dragging):
            self.dragging = False
            self.xy = mousepos
            return True
        return False
        
    def drag(self, mousepos):
        if (self.dragging):
            self.xy = mousepos
            return True
        return False
        
class DraggablePointList:
    def __init__(self, r):
        self.r = r
        self.points = {}
        
    def add(self, name, xy):
        self.points[name] = DraggablePoint(self.r, xy)
        
    def set(self, name, xy):
        self.points[name].xy = xy
        
    def remove(self, name):
        del self.points[name]
        
    def get(self, name):
        return self.points[name].xy
        
    def event(self, event, mousepos):
        for pt in self.points.values():
            if pt.event(event, mousepos):
                break