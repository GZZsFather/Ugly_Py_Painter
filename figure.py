# adapter for colorpicker in touchbar
# Inputs: the String of RGB in hex contains '#' as the begining
# Output: it returns a tuple of RGB in dec which satisfies the requirements of pygame
def ColorPicker(Object):
    R = Object[1:3]
    G = Object[3:5]
    B = Object[5:7]
    return (int(R,16),int(G,16),int(B,16))

# Line class
# Contains the basic elements for line and 4 algorithms to draw a line
# including: DDA MidPointLine bresenhamline and LineByE

class Line():
    def __init__(self,screen):
        self.screen = screen
        #default color as black
        self.color = (0,0,0)
        self.size = 1
        self.func = self.DDA

    def draw(self,start,end,func):
        self.func(start,end)

    #Interface for setting colors
    def set_color(self,color):
        self.color = color

    # Algorithm DDA
    # Input: two 2-dimensions tuple which represents the begin pixel and the end one
    # Function: draw a line between to selected pixels using DDA
    def DDA(self,start,end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        x = start[0]
        y = start[1]

        # considering of the condition that dx == 0
        # thus dx/dy is illegal
        if dx == 0:
            for i in range(dy):
                self.screen.set_at((start[0],y),self.color)
                y = y + 1
            return

        k = dy / dx

        # for 8 directions
        # in case that the line directions are different in 4 quadrant
        if dx > 0:
            arg_x = 1
        else:
            arg_x = -1
        if dy >0:
            arg_y = 1
        else:
            arg_y = -1

        # for cases which scope is less than 1 it is x that matters
        # but when sopce is greater than 1 it is y that matters
        # otherwise the line will be sparse
        if abs(k) <= 1:
            for i in range(abs(dx)):
                x = x + arg_x
                self.screen.set_at((x,int(y + 0.5*arg_y)), self.color)
                # times arg_y in case that it is in the right direction
                y = y + k * arg_x

        else:
            for i in range(abs(dy)):
                y = y + arg_y
                self.screen.set_at((int(x + 0.5*arg_x),y), self.color)
                # in inverse function the scope should be taken as reciprocal
                # times arg_y in case that it is in the right direction
                x = x + 1/k * arg_y

    # Algorithm MidPointLine
    # Input: two 2-dimensions tuple which represents the begin pixel and the end one
    # Function: draw a line between to selected pixels using MidPointLine
    def MidPointLine(self,start,end):
        # print(start,end)
        a = start[1] - end[1]
        b = end[0] - start[0]

        x = start[0]
        y = start[1]

        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # for 8 directions
        if dx > 0:
            arg_x = 1
        else:
            arg_x = -1
        if dy >0:
            arg_y = 1
        else:
            arg_y = -1

        result = (abs(dy) - abs(dx) <= abs(dx))

        self.screen.set_at((x,y),self.color)
        # for cases which scope is less than 1 it is x that matters
        # but when sopce is greater than 1 it is y that matters
        # otherwise the line will be sparse
        if(result):
            # times arg_y and arg_x in case that it is in the right direction
            a = a * arg_x
            b = b * arg_y
            d = a + a + b
            delta1 = a + a
            delta2 = a + a + b + b
            for i in range(abs(dx)):
                x = x + arg_x
                # times arg_x and arg_y is a result of derivation of this formula
                if arg_x * arg_y * d < 0:
                    # times arg_y in case that it is in the right direction
                    y = y + arg_y
                    d = d + delta2
                else:
                    d = d + delta1
                self.screen.set_at((x,y),(0,0,0))
        else:
            # a,b and d should be reset in which case y matters
            # # times arg_y and arg_x in case that it is in the right direction
            a = a * arg_x
            b = b * arg_y
            d = a + b + b
            delta1 = b + b
            delta2 = a + a + b + b
            for i in range(abs(dy)):
                y = y + arg_y
                if arg_x * arg_y * d > 0:
                    # times arg_x in case that it is in the right direction
                    x = x + arg_x
                    d = d + delta2
                else:
                    d = d + delta1
                self.screen.set_at((x,y),self.color)

    #Algorithm bresenhamline
    #Input: two 2-dimensions tuple which represents the begin pixel and the end one
    #Function: draw a line between to selected pixels using bresenhamline
    def bresenhamline(self,start,end):

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        x = start[0]
        y = start[1]

        #take the place of k
        result = (abs(dy) - abs(dx) <= abs(dx))

        # for 8 directions
        if dx > 0:
            arg_x = 1
        else:
            arg_x = -1
        if dy >0:
            arg_y = 1
        else:
            arg_y = -1

        # for cases which scope is less than 1 it is x that matters
        # but when sopce is greater than 1 it is y that matters
        # otherwise the line will be sparse
        if (result):
            e = -dx
            for i in range(abs(dx)):
                self.screen.set_at((x,y),self.color)
                x = x + arg_x
                # e should inscent with abs(dy) in case of situations in different quadrant
                e = e + 2 * abs(dy)
                if(e >= 0):
                    y = y + arg_y
                    e = e - 2 * abs(dx)
        else:
            e = -dy
            for i in range(abs(dy)):
                self.screen.set_at((x,y),self.color)
                y = y + arg_y
                e = e + 2*abs(dx)
                if(e >= 0):
                    x = x + arg_x
                    e = e - 2 * abs(dy)

    # Algorithm LineByE
    # Input: two 2-dimensions tuple which represents the begin pixel and the end one
    # Function: draw a line between to selected pixels using LineByE
    # It is just an optimization of DDA
    def LineByE(self,start,end):

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        e = -0.5
        x = start[0]
        y = start[1]
        # considering of the condition that dx == 0
        # thus dx/dy is illegal
        if dx == 0:
            for i in range(dy):
                self.screen.set_at((start[0],y),self.color)
                y = y + 1
            return

        k = dy / dx

        result = (dy - dx > dx)

        # for 8 directions
        if dx > 0:
            arg_x = 1
        else:
            arg_x = -1
        if dy >0:
            arg_y = 1
        else:
            arg_y = -1

        # for cases which scope is less than 1 it is x that matters
        # but when sopce is greater than 1 it is y that matters
        # otherwise the line will be sparse
        if (abs(k) <= 1 ):
            for i in range(abs(dx)):
                self.screen.set_at((x,y),self.color)
                x = x + arg_x
                e = e + abs(k)
                if(e >= 0):
                    y = y + arg_y
                    e = e - 1
        else:
            for i in range(abs(dy)):
                self.screen.set_at((x,y),self.color)
                y = y + arg_y
                e = e + abs(1/k)
                if(e >= 0):
                    x = x + arg_x
                    e = e - 1

# Circle class
# Contains the basic elements for the algorithms to draw a circle
class Circle():
    def __init__(self,screen):
        self.screen = screen
        #default color as black
        self.color = (0,0,0)
        self.size = 1
        self.func = self.MidPointCircle

    def draw(self,start,end,func):
        r = int (((end[0]-start[0]) ** 2 + (end[1] - start[1]) ** 2)**0.5)
        self.screen.set_at(start,ColorPicker("#FF2600"))
        self.func(start,end,r)

    def CirclePoints(self,start,end):
        x0 = start[0]
        y0 = start[1]
        x1 = end[0]
        y1 = end[1]
        dx = x1 - x0
        dy = y1 - y0
        self.screen.set_at((x1,y1),self.color)
        self.screen.set_at((x0+dy,y0+dx),self.color)
        self.screen.set_at((x0-dx,y0+dy),self.color)
        self.screen.set_at((x0+dy,y0-dx),self.color)
        self.screen.set_at((x1,y0-dy),self.color)
        self.screen.set_at((x0-dy,y0+dx),self.color)
        self.screen.set_at((x0-dx,y0-dy),self.color)
        self.screen.set_at((x0-dy,y0-dx),self.color)

    def MidPointCircle(self,start,end,r):

        x0 = start[0]
        x1 = start[1]
        x = 0
        y = r
        e = 1 - r
        self.CirclePoints(start,end)
        while(x <= y):
            if e < 0 :
                e = e + 2*x +3
            else:
                e = e + 2*(x - y) + 5
                y = y - 1

            x = x + 1

            end1 = (start[0]+x,start[1]+y)
            self.CirclePoints(start,end1)
