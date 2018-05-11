# adapter for colorpicker in touchbar
# Inputs: the String of RGB in hex contains '#' as the begining
# Output: it returns a tuple of RGB in dec which satisfies the requirements of pygame
from util import convexhull
from util import calculation
from util import getAngle
from util import getPList
import time
def ColorPicker(Object):
    R = Object[1:3]
    G = Object[3:5]
    B = Object[5:7]
    return (int(R, 16), int(G, 16), int(B, 16))


# Line class
# Contains the basic elements for line and 4 algorithms to draw a line
# including: DDA MidPointLine bresenhamline and LineByE

class Line():
    def __init__(self, screen):
        self.screen = screen
        # default color as black
        self.color = (0, 0, 0)
        self.size = 1
        self.func = self.DDA
        self.start = (0,0)
        self.end = (0,0)

    #设置颜色
    def SetColor(self,color):
        self.color=color
    def draw(self, start, end, func):
        self.func = func
        self.func(start, end)

    # Interface for setting colors
    def set_color(self, color):
        self.color = color

    # Algorithm DDA
    # Input: two 2-dimensions tuple which represents the begin pixel and the end one
    # Function: draw a line between to selected pixels using DDA
    def DDA(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        x = start[0]
        y = start[1]

        # considering of the condition that dx == 0
        # thus dx/dy is illegal
        if dx == 0:
            for i in range(dy):
                self.screen.set_at((start[0], y), self.color)
                y = y + 1
            return

        k = dy / dx

        # for 8 directions
        # in case that the line directions are different in 4 quadrant
        if dx > 0:
            arg_x = 1
        else:
            arg_x = -1
        if dy > 0:
            arg_y = 1
        else:
            arg_y = -1

        # for cases which scope is less than 1 it is x that matters
        # but when sopce is greater than 1 it is y that matters
        # otherwise the line will be sparse
        if abs(k) <= 1:
            for i in range(abs(dx)):
                x = x + arg_x
                self.screen.set_at((x, int(y + 0.5 * arg_y)), self.color)
                # times arg_y in case that it is in the right direction
                y = y + k * arg_x

        else:
            for i in range(abs(dy)):
                y = y + arg_y
                self.screen.set_at((int(x + 0.5 * arg_x), y), self.color)
                # in inverse function the scope should be taken as reciprocal
                # times arg_y in case that it is in the right direction
                x = x + 1 / k * arg_y

    # Algorithm MidPointLine
    # Input: two 2-dimensions tuple which represents the begin pixel and the end one
    # Function: draw a line between to selected pixels using MidPointLine
    def MidPointLine(self, start, end):
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
        if dy > 0:
            arg_y = 1
        else:
            arg_y = -1

        result = (abs(dy) - abs(dx) <= abs(dx))

        self.screen.set_at((x, y), self.color)
        # for cases which scope is less than 1 it is x that matters
        # but when sopce is greater than 1 it is y that matters
        # otherwise the line will be sparse
        if (result):
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
                self.screen.set_at((x, y), (0, 0, 0))
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
                self.screen.set_at((x, y), self.color)

    # Algorithm bresenhamline
    # Input: two 2-dimensions tuple which represents the begin pixel and the end one
    # Function: draw a line between to selected pixels using bresenhamline
    def BresenHamLine(self, start, end):

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        x = start[0]
        y = start[1]

        # take the place of k
        result = (abs(dy) - abs(dx) <= abs(dx))

        # for 8 directions
        if dx > 0:
            arg_x = 1
        else:
            arg_x = -1
        if dy > 0:
            arg_y = 1
        else:
            arg_y = -1

        # for cases which scope is less than 1 it is x that matters
        # but when sopce is greater than 1 it is y that matters
        # otherwise the line will be sparse
        if (result):
            e = -dx
            for i in range(abs(dx)):
                self.screen.set_at((x, y), self.color)
                x = x + arg_x
                # e should inscent with abs(dy) in case of situations in different quadrant
                e = e + 2 * abs(dy)
                if (e >= 0):
                    y = y + arg_y
                    e = e - 2 * abs(dx)
        else:
            e = -dy
            for i in range(abs(dy)):
                self.screen.set_at((x, y), self.color)
                y = y + arg_y
                e = e + 2 * abs(dx)
                if (e >= 0):
                    x = x + arg_x
                    e = e - 2 * abs(dy)

    # Algorithm LineByE
    # Input: two 2-dimensions tuple which represents the begin pixel and the end one
    # Function: draw a line between to selected pixels using LineByE
    # It is just an optimization of DDA
    def LineByE(self, start, end):

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        e = -0.5
        x = start[0]
        y = start[1]
        # considering of the condition that dx == 0
        # thus dx/dy is illegal
        if dx == 0:
            for i in range(dy):
                self.screen.set_at((start[0], y), self.color)
                y = y + 1
            return

        k = dy / dx

        result = (dy - dx > dx)

        # for 8 directions
        if dx > 0:
            arg_x = 1
        else:
            arg_x = -1
        if dy > 0:
            arg_y = 1
        else:
            arg_y = -1

        # for cases which scope is less than 1 it is x that matters
        # but when sopce is greater than 1 it is y that matters
        # otherwise the line will be sparse
        if (abs(k) <= 1):
            for i in range(abs(dx)):
                self.screen.set_at((x, y), self.color)
                x = x + arg_x
                e = e + abs(k)
                if (e >= 0):
                    y = y + arg_y
                    e = e - 1
        else:
            for i in range(abs(dy)):
                self.screen.set_at((x, y), self.color)
                y = y + arg_y
                e = e + abs(1 / k)
                if (e >= 0):
                    x = x + arg_x
                    e = e - 1


# Circle class
# Contains the basic elements for the algorithms to draw a circle
class Circle():
    def __init__(self, screen):
        self.screen = screen
        # default color as black
        self.color = (0, 0, 0)
        self.size = 1
        self.func = self.MidPointCircle

    def draw(self, start, end, func):
        r = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
        self.screen.set_at(start, self.color)
        self.func(start, end, r)
    #设置颜色
    def SetColor(self,color):
        self.color=color
    def CirclePoints(self, start, end):
        x0 = start[0]
        y0 = start[1]
        x1 = end[0]
        y1 = end[1]
        dx = x1 - x0
        dy = y1 - y0
        self.screen.set_at((x1, y1), self.color)
        self.screen.set_at((x0 + dy, y0 + dx), self.color)
        self.screen.set_at((x0 - dx, y0 + dy), self.color)
        self.screen.set_at((x0 + dy, y0 - dx), self.color)
        self.screen.set_at((x1, y0 - dy), self.color)
        self.screen.set_at((x0 - dy, y0 + dx), self.color)
        self.screen.set_at((x0 - dx, y0 - dy), self.color)
        self.screen.set_at((x0 - dy, y0 - dx), self.color)

    def MidPointCircle(self, start, end, r):

        x0 = start[0]
        x1 = start[1]
        x = 0
        y = r
        e = 1 - r
        self.CirclePoints(start, end)
        while (x <= y):
            if e < 0:
                e = e + 2 * x + 3
            else:
                e = e + 2 * (x - y) + 5
                y = y - 1

            x = x + 1

            end1 = (start[0] + x, start[1] + y)
            self.CirclePoints(start, end1)

#class polygon
class Polygon():
    def __init__(self,screen):
        self.screen=screen
        self.color=(0,0,0)
        self.size=1
        self.func=self.FillPolygonPbyP
        self.IsInside=self.radial
        self.listpoint = []
    #画图函数
    def draw(self,listpoint):
        self.func(listpoint)
    #设置颜色函数
    def SetColor(self,color):
        self.color=color
    #逐点判断法
    def FillPolygonPbyP(self,listpoint):
        #x轴的列表
        x_list=[x[0] for x in listpoint]
        #y轴的列表
        y_list=[x[1] for x in listpoint]
        xmin=min(x_list)
        xmax=max(x_list)+1
        ymin=min(y_list)
        ymax=max(y_list)+1
        for y in range(ymin,ymax):
            for x in range(xmin,xmax):
                point=(x,y)
                if(self.IsInside(listpoint,point)):
                    self.screen.set_at((x,y),self.color)

    def radial(self,listpoint,point):
        #经过多边形的边数
        n=0
        length=len(listpoint)
        for i in range(length):
            p1=p2=p3=(0,0)
            if i==length-1:
                p1=listpoint[-1]
                p2=listpoint[0]
            else:
                p1=listpoint[i]
                p2=listpoint[i+1]
            #如果
            if p2[1]==point[1]:
                p3=listpoint[(i+2)%length]
                dy1=p1[1]-p2[1]
                dy2=p3[1]-p2[1]
                if dy1*dy2<0 and point[0]<p2[0]:
                    n+=1
                else:
                    n+=0
            elif p1[1]==point[1]:
                n+=0
            else:
                if p1[1]>p2[1]:
                    p1,p2=p2,p1
                n+=calculation(p1,p2,point)
            #print("{},{}:{}={}".format(p1,p2,point,n))
        if n%2==1:
            return True
        else:
            return False
    #累计角度法
    def Accumulative(self,listpoint,point):
        angle=0
        lenght=len(listpoint)
        for i in range(lenght):
            p1=p2=p3=(0,0)
            if i==lenght-1:
                p1=listpoint[-1]
                p2=listpoint[0]
            else:
                p1=listpoint[i]
                p2=listpoint[i+1]
            #计算角度
            angle+=getAngle(p1,p2,point)
        if 6.18<angle<6.3:
            return True
        return False
    #编码法
    def Code(self,listpoint,point):
        pass
    #扫描算法填充
    def FillPolygonScan(self,listpoint):
        y_list=[x[1] for x in listpoint]
        ymin=min(y_list)
        ymax=max(y_list)+1
        for y in range(ymin,ymax):
            plist=getPList(y,listpoint)
            line=Line(self.screen)
            length=len(plist)
            if length%2==1:
                time.sleep(30)
            for i in range(0,length,2):
                line.DDA(plist[i],plist[i+1])


    def getPList(y,listpoint):
        pass
#cutting
if __name__ == '__main__':
    listpoint=[(1,0),(2,0),(2,1),(3,1),
    (3,2),(2,2),(2,3),(1,3),
    (1,2),(0,2),(0,1),(1,1),]
    listpoint=[(point[0]*2,point[1]*2) for point in listpoint]
    print(listpoint)
    while True:
        myinput=input("请输入要查询的点：")
        myinput=myinput.split()
        point=(int(myinput[0]),int(myinput[1]))
        print(point)
        if Polygon.Accumulative(listpoint,point):
            print("在图像内")
        else:
            print("在图像外")
