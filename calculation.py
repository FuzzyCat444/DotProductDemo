import math

def intersect_lines(p0, p1, p2, p3):
    (x0, y0) = p0
    (x1, y1) = p1
    (x2, y2) = p2
    (x3, y3) = p3
    dx0 = x1 - x0
    dy0 = y1 - y0
    dx1 = x3 - x2
    dy1 = y3 - y2
    
    denom = dx0 * dy1 - dy0 * dx1
    if denom == 0:
        return (0, 0)
    t = (dy1 * (x2 - x0) - dx1 * (y2 - y0)) / denom
              
    
    return (x0 + t * dx0, y0 + t * dy0)
    
# Returns > 0 if counterclockwise to line, < 0 if clockwise to line, 0 if on line
def point_counterclockwise_to_line(p, linep0, linep1):
    (px, py) = p
    (x0, y0) = linep0
    (x1, y1) = linep1
    (px, py) = (px - x0, py - y0)
    (vx, vy) = (x1 - x0, y1 - y0)
    
    return vx * py - vy * px
    
def dot(v0, v1):
    (x0, y0) = v0
    (x1, y1) = v1
    
    return x0 * x1 + y0 * y1
    
def anglebetween(v0, v1):
    dt = dot(v0, v1)
    cos = dt / (lenv(v0) * lenv(v1))
    return math.acos(cos)
    
def angle(v):
    (x, y) = v
    return math.atan2(y, x) % math.tau
    
def vecfromangle(a):
    return (cos(a), sin(a))

def norm(v):
    length = lenv(v)
    if length == 0:
        return (0, 0)
    return scalevec(1 / length, v)
    
def lenv(v):
    return math.sqrt(lenvsq(v))
    
def lenvsq(v):
    (x, y) = v
    return x ** 2 + y ** 2

def projection(v0, v1):
    len2 = lenvsq(v1)
    if len2 == 0:
        return (0, 0)
    mul = dot(v0, v1) / len2
    
    return scalevec(mul, v1)
    
def vecx(v):
    (x, y) = v
    return x
    
def vecy(v):
    (x, y) = v
    return y
    
def addvecs(v0, v1):
    (x0, y0) = v0
    (x1, y1) = v1
    
    return (x0 + x1, y0 + y1)
    
def subvecs(v0, v1):
    (x0, y0) = v0
    (x1, y1) = v1
    
    return (x0 - x1, y0 - y1)
    
def scalevec(s, v):
    (x, y) = v
    
    return (s * x, s * y)
    
def rotate90cc(v):
    (x, y) = v
    return (-y, x)
    
def rotate90c(v):
    (x, y) = v
    return (y, -x)