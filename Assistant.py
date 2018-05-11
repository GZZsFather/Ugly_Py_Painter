import pygame
from pygame.locals import *
ZERO = 1e-9
INF = 1000000


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        # signals for WA to decide wheter the line gets in the figure or out
        # 1 represents in  0 represents out 4 represents this point doen't matter
        self.get_in = 3

class Vector(object):
    def __init__(self, start_point, end_point):
        self.start, self.end = start_point, end_point
        self.x = end_point.x - start_point.x
        self.y = end_point.y - start_point.y

def negative(vector):
    return Vector(vector.end,vector.start)

def vector_product(vectorA,vectorB):
    return vectorA.x*vectorB.y -vectorB.x*vectorA.y

def isIntersected(A,B,C,D):
    AC = Vector(A,C)
    AD = Vector(A,D)
    BC = Vector(B,C)
    BD = Vector(B,D)
    CA = negative(AC)
    CB = negative(BC)
    DA = negative(AD)
    DB = negative(BD)

    return (vector_product(AC, AD) * vector_product(BC, BD) <= ZERO) \
        and (vector_product(CA, CB) * vector_product(DA, DB) <= ZERO)


def PL_distance(line,point):
    A = line[0]
    B = line[1]
    
    a0 = A.y - B.y
    b0 = B.x - A.x
    c0 = A.x * B.y - B.x * A.y

    d = abs(a0 * point.x + b0 * point.y + c0)/((a0**2+b0**2)**0.5)

    return d

def FindPointIndex(list,point):
    for i in range(len(list)):
        if list[i].x == point.x and list[i].y == point.y:
            return i
    print("Not found!")

def trans_pointlist(pointlist_inter,margin_inter,Q,start):
    start_index = pointlist_inter.index(start)
    
    i = start_index
    flag = False
    while i < len(pointlist_inter):
        point = pointlist_inter[i]
        now = i
        print("Now trans_pointlist at point (%d,%d) i = %d"%(point.x,point.y,i))
        if point.get_in == 1:
            Q.append(point)
            i = i + 1
            flag = True
        elif point.get_in ==3:
            i = i + 1
            if flag:
                Q.append(point)
        else:
            flag = False
            margin_start = FindPointIndex(margin_inter,point)
            print("Now jump to margin at point (%d,%d) i = %d"%(point.x,point.y,i))
            print("Start Margin = %d"%margin_start)
            result= trans_margin(pointlist_inter,margin_inter,Q,margin_inter[margin_start])
            if result is None:
                print("Error")
                return
            else:
                Q, tmp = result
                if tmp >= i:
                    i = tmp
                else:
                    i = now + 1
                    Q.append(Point(INF,INF))
                    
    return Q

def trans_margin(pointlist_inter,margin_inter,Q,start):
    start_index = margin_inter.index(start)
    i = start_index
    count = 0
    
    while i < len(margin_inter):
        point = margin_inter[i]        
        print("get_in = %d"%point.get_in)
        print("Now trans_margin at point (%d,%d) i = %d"%(point.x,point.y,i))
        if point.get_in != 1:
            Q.append(point)
            if i == len(margin_inter) -1 and count < 1:
                count = count + 1
                print("count reset!")
                i = 0
                continue
            i = i + 1
        else:
            #  trans_start = pointlist_inter.index(point)
            trans_start = FindPointIndex(pointlist_inter,point)
            print("Back to trans_pointlist and trans_start = %d"%trans_start)
            print("margin_inter len = %d"%len(margin_inter))

            # if i == len(margin_inter) -1 and count < 1:
            #     count = count + 1
            #     print("count reset!")
            #     i = 0
            #     continue
            # else:
            return Q,trans_start
        


def WA_Cutting(pointlist_inter,margin_inter):
    Q = []
    start = pointlist_inter[0]
    Q = trans_pointlist(pointlist_inter,margin_inter,Q,start)
    return Q


def intersection_point(A,B,C,D):
    a0 = A.y - B.y
    b0 = B.x - A.x
    c0 = A.x * B.y - B.x * A.y
    a1 = C.y - D.y
    b1 = D.x - C.x
    c1 = C.x * D.y - D.x * C.y
    d = 0
    if B.x - A.x != 0:
        d = (B.y-A.y)/(B.x-A.x)
    D = a0*b1 - a1*b0
    if(D != 0):
        x = (b0*c1 - b1*c0)/D
        y = (a1*c0 - a0*c1)/D

        if(abs(d) < 1):
            result = Point(int(x),int(y+0.5))
        elif(abs(d) > 1):
            result = Point(int(x+0.5),int(y))
        else:
            result = Point(int(x),int(y))
        return result



class Button():
    def __init__(self, upimage, downimage,position,screen):
        img1 = pygame.image.load(upimage).convert_alpha()
        img2 = pygame.image.load(downimage).convert_alpha()
        self.imageUp = pygame.transform.scale(img1,(50,20))
        self.imageDown = pygame.transform.scale(img2,(50,20))
        self.position = position
        self.screen = screen
        self.selected = False
        self.front_image = self.imageUp

    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.imageUp.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def render(self):
        w, h = self.imageUp.get_size()
        x, y = self.position

        if self.isOver():
            self.screen.blit(self.imageDown, (x-w/2,y-h/2))
        else:
            self.screen.blit(self.front_image, (x-w/2, y-h/2))



class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.colors = [
            (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
            (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
            (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
            (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
            (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
            (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
            (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
            (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
        ]

        self.lines = [
            pygame.image.load("./icons/DDA.png").convert_alpha(),
            pygame.image.load("./icons/MPL.png").convert_alpha(),
            pygame.image.load("./icons/BRE.png").convert_alpha(),
            pygame.image.load("./icons/LBE.png").convert_alpha(),

        ]
        self.lines_rect = []
        for (i, img) in enumerate(self.lines):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.lines_rect.append(rect)


        self.colors_rect = []
        for (i, rgb) in enumerate(self.colors):
            rect = pygame.Rect(10 + i % 2 * 32, 254 + i / 2 * 32, 32, 32)
            self.colors_rect.append(rect)
        self.lines = None

    def draw(self):
        # draw pen style button
        for (i, img) in enumerate(self.lines):
          self.screen.blit(img, self.lines_rect[i].topleft)

        self.screen.fill((255, 255, 255), (10, 180, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 180, 64, 64), 1)

        for (i, rgb) in enumerate(self.colors):
          pygame.draw.rect(self.screen, rgb, self.colors_rect[i])

    def click_button(self,pos):
        #DDA button
        for (i, rect) in enumerate(self.lines_rect):
            if rect.collidepoint(pos):
                self.line.set_line_style(i)
                return True
        #colors button
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.line.set_color(self.colors[i])
                return True
            return False
