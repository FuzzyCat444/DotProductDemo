import pygame
import math

from visual import *
from interaction import *
from calculation import *

class Demo:
    def __init__(self):
        # Change these variables only
        self.size = (1700, 900)
        self.origin = (350, 100)
        self.vec_a = (700, 0)
        self.vec_b = (500, 0)
        self.prooflocation = (1000, 800)
        self.fontsize = 30
        self.pixelsperunit = 100
        
        self.vec_a_x = (0, 0)
        self.vec_a_y = (0, 0)
        self.neg_vec_a_x = (0, 0)
        self.neg_vec_a_y = (0, 0)
        self.vec_b_x = (0, 0)
        self.vec_b_y = (0, 0)
        self.neg_vec_b_x = (0, 0)
        self.neg_vec_b_y = (0, 0)
        self.proj_start = (0, 0)
        self.proj_end = (0, 0)
        self.proj = (0, 0)
        self.neg_proj = (0, 0)
        self.proj_y = (0, 0)
        self.proj_x = (0, 0)
        self.neg_proj_y = (0, 0)
        self.neg_proj_x = (0, 0)
        self.proj_y_perp = (0, 0)
        self.proj_x_perp = (0, 0)
        self.neg_proj_y_perp = (0, 0)
        self.neg_proj_x_perp = (0, 0)
        self.proj_y_pt = (0, 0)
        self.proj_x_pt = (0, 0)
        self.vec_b_end = (0, 0)
        self.vec_a_end = (0, 0)
        self.perp_vec = (0, 0)
        self.neg_perp_vec = (0, 0)
        self.neg_a = (0, 0)
        self.neg_b = (0, 0)
        self.vec_b_xy_corner = (0, 0)
        self.vec_a_xy_corner = (0, 0)
        
        self.vec_arrow_w = 12
        self.vec_arrow_h = 20
        self.bgcolor = (248, 252, 222)
        self.a_color = (204, 49, 49)
        self.b_color = (0, 199, 33)
        self.pink_tri_color = (212, 0, 255)
        self.purple_tri_color = (102, 0, 255)
        self.blue_tri_color = (0, 200, 214)
        self.prooftextcolor = (0, 0, 0)
        self.labelcolor = (0, 0, 0)
        self.labelbgcolor = self.bgcolor
        self.similar_angle_1_color = (255, 94, 94)
        self.similar_angle_2_color = (145, 255, 143)
        self.similar_angle_3_color = (89, 156, 255)
        self.angle_between_ab_color = (181, 179, 49)
        self.projection_color = (219, 173, 55)
        
        self.screen = pygame.Surface(self.size)
        self.done = False
        self.font = None
        self.draggablepointlist = DraggablePointList(20)
        self.draggablepointlist.add("vec_a_pt", addvecs(self.origin, self.vec_a))
        self.draggablepointlist.add("vec_b_pt", addvecs(self.origin, self.vec_b))
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            else:
                (mx, my) = pygame.mouse.get_pos()
                self.draggablepointlist.event(event, (mx, vecy(self.size) - my))
                
    def constraints(self):
        vec_a_pt = self.draggablepointlist.get("vec_a_pt")
        vec_b_pt = self.draggablepointlist.get("vec_b_pt")
        
        # Limit vec a and vec b to positive xy
        if vecx(vec_a_pt) < vecx(self.origin):
            vec_a_pt = (vecx(self.origin), vecy(vec_a_pt))
        if vecy(vec_a_pt) < vecy(self.origin):
            vec_a_pt = (vecx(vec_a_pt), vecy(self.origin))
        if vecx(vec_b_pt) < vecx(self.origin):
            vec_b_pt = (vecx(self.origin), vecy(vec_b_pt))
        if vecy(vec_b_pt) < vecy(self.origin):
            vec_b_pt = (vecx(vec_b_pt), vecy(self.origin))
            
        # Limit vec b to be above vec a
        perpvec = rotate90cc(subvecs(vec_a_pt, self.origin))
        if point_counterclockwise_to_line(vec_b_pt, self.origin, vec_a_pt) < 0:
            vec_b_pt = intersect_lines(vec_b_pt, subvecs(vec_b_pt, perpvec), self.origin, vec_a_pt)
        
        # Limit vec b projection to vec a
        perpend = addvecs(vec_a_pt, perpvec)
        if point_counterclockwise_to_line(vec_b_pt, vec_a_pt, perpend) < 0:
            vec_b_pt = intersect_lines(self.origin, vec_b_pt, vec_a_pt, perpend)
        
        self.draggablepointlist.set("vec_a_pt", vec_a_pt)
        self.draggablepointlist.set("vec_b_pt", vec_b_pt)
        
    def getpoints(self):
        vec_a_pt = self.draggablepointlist.get("vec_a_pt")
        vec_b_pt = self.draggablepointlist.get("vec_b_pt")
        self.vec_a = subvecs(vec_a_pt, self.origin)
        self.vec_b = subvecs(vec_b_pt, self.origin)
        
    def computations(self):
        self.vec_b_end = addvecs(self.origin, self.vec_b)
        self.vec_a_end = addvecs(self.origin, self.vec_a)
        self.proj = projection(self.vec_b, self.vec_a)
        self.neg_proj = scalevec(-1, self.proj)
        self.proj_start = self.origin
        self.proj_end = addvecs(self.origin, self.proj)
        self.vec_b_xy_corner = addvecs(self.origin, (0, vecy(self.vec_b)))
        self.vec_a_xy_corner = addvecs(self.origin, (vecx(self.vec_a), 0))
        self.perp_vec = subvecs(self.proj_end, self.vec_b_end)
        self.neg_perp_vec = scalevec(-1, self.perp_vec)
        self.neg_a = scalevec(-1, self.vec_a)
        self.neg_b = scalevec(-1, self.vec_b)
        self.vec_a_x = (vecx(self.vec_a), 0)
        self.vec_a_y = (0, vecy(self.vec_a))
        self.neg_vec_a_x = scalevec(-1, self.vec_a_x)
        self.neg_vec_a_y = scalevec(-1, self.vec_a_y)
        self.vec_b_x = (vecx(self.vec_b), 0)
        self.vec_b_y = (0, vecy(self.vec_b))
        self.neg_vec_b_x = scalevec(-1, self.vec_b_x)
        self.neg_vec_b_y = scalevec(-1, self.vec_b_y)
        lena = lenv(self.vec_a)
        if lena == 0:
            lena = 1
        self.proj_y = scalevec(-vecy(self.vec_a) * vecy(self.vec_b) / lena, norm(self.proj))
        self.proj_x = scalevec(vecx(self.vec_a) * vecx(self.vec_b) / lena, norm(self.proj))
        self.neg_proj_y = scalevec(-1, self.proj_y)
        self.neg_proj_x = scalevec(-1, self.proj_x)
        self.proj_y_pt = addvecs(self.vec_b_xy_corner, self.proj_y)
        self.proj_x_pt = addvecs(self.vec_b_xy_corner, self.proj_x)
        self.proj_y_perp = subvecs(self.origin, self.proj_y_pt)
        self.proj_x_perp = subvecs(self.vec_b_end, self.proj_x_pt)
        self.neg_proj_y_perp = scalevec(-1, self.proj_y_perp)
        self.neg_proj_x_perp = scalevec(-1, self.proj_x_perp)
    
    def update(self):
        self.constraints()
        self.getpoints()
        self.computations()
        
    def draw(self):
        # Axes
        SegmentVisual((0, vecy(self.origin)), (vecx(self.size), vecy(self.origin)), (0, 0, 0), 1).draw(self.screen)
        SegmentVisual((vecx(self.origin), 0), (vecx(self.origin), vecy(self.size)), (0, 0, 0), 1).draw(self.screen)
    
        # x projection triangle area
        AreaVisual((181, 141, 240), [self.vec_b_xy_corner, self.proj_x_pt, self.vec_b_end]).draw(self.screen)
        # y projection triangle area
        AreaVisual((243, 186, 255), [self.vec_b_xy_corner, self.proj_y_pt, self.origin]).draw(self.screen)
        # vec a x and y triangle area
        AreaVisual((176, 250, 255), [self.origin, self.vec_a_xy_corner, self.vec_a_end]).draw(self.screen)
    
        # angle between a and ax
        AngleVisual(self.origin, self.vec_a, self.vec_a_x, 35, (0, 0, 0), self.similar_angle_1_color, 4).draw(self.screen)
        # angle between a and ay
        AngleVisual(self.vec_a_end, self.neg_a, self.neg_vec_a_y, 35, (0, 0, 0), self.similar_angle_3_color, 4).draw(self.screen)
        # angle between ax and ay
        AngleVisual(self.vec_a_xy_corner, self.neg_vec_a_x, self.vec_a_y, 35, (0, 0, 0), self.similar_angle_2_color, 4).draw(self.screen)
        # angle between proj y and by
        AngleVisual(self.vec_b_xy_corner, self.proj_y, self.neg_vec_b_y, 35, (0, 0, 0), self.similar_angle_3_color, 4).draw(self.screen)
        # angle between proj x and bx
        AngleVisual(self.vec_b_xy_corner, self.proj_x, self.vec_b_x, 35, (0, 0, 0), self.similar_angle_1_color, 4).draw(self.screen)
        # angle between proj y and proj y perp
        AngleVisual(self.proj_y_pt, self.proj_y_perp, self.neg_proj_y, 35, (0, 0, 0), self.similar_angle_2_color, 4).draw(self.screen)
        # angle between proj x and proj x perp
        AngleVisual(self.proj_x_pt, self.proj_x_perp, self.neg_proj_x, 35, (0, 0, 0), self.similar_angle_2_color, 4).draw(self.screen)
        # angle between proj y perp and by
        AngleVisual(self.origin, self.neg_proj_y_perp, self.vec_b_y, 35, (0, 0, 0), self.similar_angle_1_color, 4).draw(self.screen)
        # angle between proj x perp and bx
        AngleVisual(self.vec_b_end, self.neg_proj_x_perp, self.neg_vec_b_x, 35, (0, 0, 0), self.similar_angle_3_color, 4).draw(self.screen)
        
        # angle between a and b
        AngleVisual(self.origin, self.proj, self.vec_b, 45, (0, 0, 0), self.angle_between_ab_color, 4).draw(self.screen)
        # angle between b and perpendicular
        AngleVisual(self.vec_b_end, self.neg_b, self.perp_vec, 35, (0, 0, 0), None, 4).draw(self.screen)
        # angle between a and perpendicular
        AngleVisual(self.proj_end, self.neg_proj, self.neg_perp_vec, 35, (0, 0, 0), None, 4).draw(self.screen)
        # angle between x and y of b
        AngleVisual(self.vec_b_xy_corner, self.neg_vec_b_y, self.vec_b_x, 35, (0, 0, 0), None, 4).draw(self.screen)
        # angle between y of b and b
        AngleVisual(self.origin, self.vec_b_y, self.vec_b, 35, (0, 0, 0), None, 4).draw(self.screen)
        # angle between x of b and b
        AngleVisual(self.vec_b_end, self.neg_vec_b_x, self.neg_b, 35, (0, 0, 0), None, 4).draw(self.screen)
        
        if vecx(self.vec_b) > 0 and vecy(self.vec_b) > 0:
            # x component of vector b
            SegmentVisual(self.vec_b_end, self.vec_b_xy_corner, self.purple_tri_color, 4, "Bx", self.font, self.labelcolor, self.labelbgcolor).draw(self.screen)
            # y component of vector b
            SegmentVisual(self.origin, self.vec_b_xy_corner, self.pink_tri_color, 4, "By", self.font, self.labelcolor, self.labelbgcolor).draw(self.screen)
        if vecx(self.vec_a) > 0 and vecy(self.vec_a) > 0:
            # x component of vector a
            SegmentVisual(self.origin, self.vec_a_xy_corner, self.blue_tri_color, 4, "Ax", self.font, self.labelcolor, self.labelbgcolor).draw(self.screen)
            # y component of vector a
            SegmentVisual(self.vec_a_xy_corner, self.vec_a_end, self.blue_tri_color, 4, "Ay", self.font, self.labelcolor, self.labelbgcolor).draw(self.screen)
            # y projection of b onto a
            SegmentVisual(self.vec_b_xy_corner, self.proj_y_pt, self.pink_tri_color, 4, "C", self.font, self.labelcolor, self.labelbgcolor).draw(self.screen)
            # x projection of b onto a
            SegmentVisual(self.vec_b_xy_corner, self.proj_x_pt, self.purple_tri_color, 4, "D", self.font, self.labelcolor, self.labelbgcolor).draw(self.screen)
            # y projection perpendicular of b onto a
            SegmentVisual(self.origin, self.proj_y_pt, self.pink_tri_color, 4).draw(self.screen)
            # x projection perpendicular of b onto a
            SegmentVisual(self.vec_b_end, self.proj_x_pt, self.purple_tri_color, 4).draw(self.screen)
        # vector projection perpendicular of b onto a
        SegmentVisual(self.vec_b_end, self.proj_end, (0, 0, 0), 2).draw(self.screen)
        # vector a
        VectorVisual(self.origin, self.vec_a, self.a_color, self.vec_arrow_w, self.vec_arrow_h, 4).draw(self.screen)
        # projection of b onto a
        SegmentVisual(self.proj_start, self.proj_end, self.projection_color, 8, "P", self.font, self.labelcolor, self.labelbgcolor).draw(self.screen)
        # vector b
        VectorVisual(self.origin, self.vec_b, self.b_color, self.vec_arrow_w, self.vec_arrow_h, 4).draw(self.screen)
        
        
        # Proof
        prooflineloc = self.prooflocation
        linedownvec = (0, vecy(self.font.size("Oq")) * 1.5)
        linerightvec = (0, 0)
        sent = ""
        
        def sentence(text, color):
            nonlocal linerightvec
            TextVisual(addvecs(prooflineloc, linerightvec), text, self.font, color).draw(self.screen)
            linerightvec = addvecs(linerightvec, (vecx(self.font.size(text)), 0))
        
        def nextline():
            nonlocal linerightvec
            nonlocal prooflineloc
            linerightvec = (0, 0)
            prooflineloc = subvecs(prooflineloc, linedownvec)
        
        sentence("Proof: show that the algebraic and geometric", self.prooftextcolor)
        nextline()
        sentence("definitions of the dot product are equivalent.", self.prooftextcolor)
        
        # Line 1
        nextline()
        nextline()
        sentence("A is a vector", self.a_color)
        sentence(" and", self.prooftextcolor)
        sentence(" B is a vector", self.b_color)
        sentence(" and", self.prooftextcolor)
        sentence(" \u03B8 is the angle between the two", self.angle_between_ab_color)
        sentence(".", self.prooftextcolor)
        # Line 2
        nextline()
        sentence("\u0394", self.pink_tri_color)
        sentence(" and", self.prooftextcolor)
        sentence(" \u0394", self.purple_tri_color)
        sentence(" and", self.prooftextcolor)
        sentence(" \u0394", self.blue_tri_color)
        sentence(" are similar triangles and are in proportion.", self.prooftextcolor)
        # Line 3
        nextline()
        sentence("P", self.projection_color)
        sentence(" =", self.prooftextcolor)
        sentence(" D", self.purple_tri_color)
        sentence(" +", self.prooftextcolor)
        sentence(" C", self.pink_tri_color)
        sentence(" =", self.prooftextcolor)
        sentence(" |B|", self.b_color)
        sentence("cos\u03B8", self.angle_between_ab_color)
        # Line 4
        nextline()
        sentence("D", self.purple_tri_color)
        sentence(" /", self.prooftextcolor)
        sentence(" Bx", self.purple_tri_color)
        sentence(" =", self.prooftextcolor)
        sentence(" Ax", self.blue_tri_color)
        sentence(" /", self.prooftextcolor)
        sentence(" |A|", self.a_color)
        sentence("   and", self.prooftextcolor)
        sentence("    C", self.pink_tri_color)
        sentence(" /", self.prooftextcolor)
        sentence(" By", self.pink_tri_color)
        sentence(" =", self.prooftextcolor)
        sentence(" Ay", self.blue_tri_color)
        sentence(" /", self.prooftextcolor)
        sentence(" |A|", self.a_color)
        sentence("   because similar triangles.", self.prooftextcolor)
        # Line 5
        nextline()
        sentence("D", self.purple_tri_color)
        sentence(" =", self.prooftextcolor)
        sentence(" Ax", self.blue_tri_color)
        sentence("Bx", self.purple_tri_color)
        sentence(" /", self.prooftextcolor)
        sentence(" |A|", self.a_color)
        sentence("   and", self.prooftextcolor)
        sentence("   C", self.pink_tri_color)
        sentence(" =", self.prooftextcolor)
        sentence(" Ay", self.blue_tri_color)
        sentence("By", self.pink_tri_color)
        sentence(" /", self.prooftextcolor)
        sentence(" |A|", self.a_color)
        # Line 6
        nextline()
        sentence("Ax", self.blue_tri_color)
        sentence("Bx", self.purple_tri_color)
        sentence(" /", self.prooftextcolor)
        sentence(" |A|", self.a_color)
        sentence(" +", self.prooftextcolor)
        sentence(" Ay", self.blue_tri_color)
        sentence("By", self.pink_tri_color)
        sentence(" /", self.prooftextcolor)
        sentence(" |A|", self.a_color)
        sentence(" =", self.prooftextcolor)
        sentence(" |B|", self.b_color)
        sentence("cos\u03B8", self.angle_between_ab_color)
        sentence("   after substitution.", self.prooftextcolor)
        # Line 7
        nextline()
        sentence("Ax", self.blue_tri_color)
        sentence("Bx", self.purple_tri_color)
        sentence(" +", self.prooftextcolor)
        sentence(" Ay", self.blue_tri_color)
        sentence("By", self.pink_tri_color)
        sentence(" =", self.prooftextcolor)
        sentence(" |A|", self.a_color)
        sentence("|B|", self.b_color)
        sentence("cos\u03B8", self.angle_between_ab_color)
        sentence("   done.", self.prooftextcolor)
        # Line 8
        nextline()
        nextline()
        sentence("          A", self.a_color)
        sentence(" = ({:.2f}, {:.2f})".format(vecx(self.vec_a) / self.pixelsperunit, vecy(self.vec_a) / self.pixelsperunit), self.prooftextcolor)
        # Line 9
        nextline()
        sentence("          B", self.b_color)
        sentence(" = ({:.2f}, {:.2f})".format(vecx(self.vec_b) / self.pixelsperunit, vecy(self.vec_b) / self.pixelsperunit), self.prooftextcolor)
        # Line 10
        nextline()
        sentence("          P", self.projection_color)
        sentence(" = (", self.prooftextcolor)
        sentence("Ax", self.blue_tri_color)
        sentence("Bx", self.purple_tri_color)
        sentence(" +", self.prooftextcolor)
        sentence(" Ay", self.blue_tri_color)
        sentence("By", self.pink_tri_color)
        sentence(") /", self.prooftextcolor)
        sentence(" |A|", self.a_color)
        sentence(" =", self.prooftextcolor)
        sentence(" |B|", self.b_color)
        sentence("cos\u03B8", self.angle_between_ab_color)
        sentence(" =", self.prooftextcolor)
        sentence(" {:.2f}".format(lenv(self.proj) / self.pixelsperunit), self.prooftextcolor)
    
    def start(self):
        self.init()
        displaysurface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Dot Product Demo")
        
        self.font = pygame.font.Font(None, self.fontsize)
        
        self.done = False
        clock = pygame.time.Clock()
        
        while not self.done:
            self.events()
         
            self.update()
            
            self.screen.fill(self.bgcolor)
            self.draw()
            self.screen = pygame.transform.flip(self.screen, False, True)
            displaysurface.blit(self.screen, (0, 0))
            pygame.display.flip()
            
            clock.tick(1000)
        self.quit()
        
    def init(self):
        pygame.init()
        pygame.font.init()
    
    def quit(self):
        pygame.font.quit()
        pygame.quit()