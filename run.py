
from pygame.locals import *
from Assistant import *
from figure import *


def ColorPicker(Object):
    R = Object[1:3]
    G = Object[3:5]
    B = Object[5:7]
    return (int(R,16),int(G,16),int(B,16))


class Painter():
    def __init__(self):
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption("Painter")
        self.clock = pygame.time.Clock()
        # self.brush = Brush(self.screen)
        self.line = Line(self.screen)
        self.circle = Circle(self.screen)
        self.polygon=Polygon(self.screen)
        # self.menu = Menu(self.screen)
        self.drawing = False
        self.figure = self.line
        self.selected_button = None
        self.listpoint=[]
        self.Margin = []
        self.origin_point = []
        self.Margin_point = []
        self.intersection_point = []
        self.figurelist=[]
        self.notfilling = False
        self.IsCutting=False


    def run(self):
        self.screen.fill((255,255,255))
        start = None
        end = None
        

        button_DDA = Button("./icons/DDA.png","./icons/MPL.png",(50,50),self.screen)
        button_BRE = Button("./icons/BRE.png","./icons/MPL.png",(50,70),self.screen)
        button_LBE = Button("./icons/LBE.png","./icons/MPL.png",(50,90),self.screen)
        button_MPL = Button("./icons/MPL.png","./icons/MPL.png",(50,110),self.screen)
        button_Cir = Button("./icons/Cir.png","./icons/MPL.png",(50,130),self.screen)
        button_FillRadial=Button("./icons/RAL.png","./icons/MPL.png",(50,150),self.screen)
        button_FillAA=Button("./icons/AccumulativeAngle.png","./icons/MPL.png",(50,170),self.screen)
        button_FillCode=Button("./icons/Code.png","./icons/MPL.png",(50,190),self.screen)
        button_FillPolygonScan=Button("./icons/FLS.png","./icons/MPL.png",(50,210),self.screen)
        button_clear=Button("./icons/clear.png","./icons/clear.png",(50,230),self.screen)
        button_Cutting=Button("./icons/draw.png","./icons/cutting.png",(50,250),self.screen)
        button_Polygon=Button("./icons/FLS.png","./icons/MPL.png",(50,270),self.screen)
        # a list to iterate the buttons
        button_list = [button_DDA,button_BRE,button_LBE,button_MPL,]
        # dictation for selecting algorithm
        button_dic = {button_DDA:self.line.DDA,
        button_BRE:self.line.BresenHamLine,
        button_LBE:self.line.LineByE,
        button_MPL:self.line.MidPointLine,
        }
        #图像填充按钮
        button_fill_list=[button_FillRadial,button_FillAA,button_FillCode,button_FillPolygonScan]
        button_fill_dic={button_FillRadial:(self.polygon.FillPolygonPbyP,self.polygon.radial),
        button_FillAA:(self.polygon.FillPolygonPbyP,self.polygon.Accumulative),
        button_FillCode:(self.polygon.FillPolygonPbyP,self.polygon.Code),
        button_FillPolygonScan:(self.polygon.FillPolygonScan,None)}


        #lists for WA-Cutting
        listpoint_inter = []
        Margin_inter = []
        listpoint_point = []
        # Margin_point = []


        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

                elif event.type == MOUSEBUTTONUP:
                    # self.brush.end_draw()
                    pass

                elif event.type == MOUSEBUTTONDOWN:
                    if self.IsCutting:
                        self.figure = self.polygon
                        self.Margin.append(event.pos)
                        # self.Margin_point.append(Point(event.pos[0],event.pos[1]))
                        self.line.SetColor(ColorPicker("#00F900"))

                        if len(self.Margin)>1:
                            self.line.draw(self.Margin[-2],self.Margin[-1],self.line.LineByE)
                        if event.button == 3:
                            self.line.draw(self.Margin[-2],self.Margin[-1],self.line.LineByE)
                            self.line.draw(self.Margin[-1],self.Margin[0],self.line.LineByE)

                            for item in self.listpoint:
                                self.origin_point.append(Point(item[0],item[1]))

                            for item in self.Margin:
                                self.Margin_point.append(Point(item[0],item[1]))


                            for i in range(len(self.listpoint)):

                                first_inter = False
                                start = listpoint_point[i]
                                if i == len(self.listpoint) - 1:
                                    end = listpoint_point[0]
                                else:
                                    end = listpoint_point[i+1]

                                listpoint_inter.append(start)

                                IsInside1 = self.figure.Accumulative(self.Margin,(start.x,start.y))

                                if not first_inter and not IsInside1:
                                    get_in = 1
                                else:
                                    get_in = 0
                                
                                tmp = []
                                for j in range(len(self.Margin)):
                                    start1 = self.Margin_point[j]
                                    if j == len(self.Margin) - 1:
                                        end1 = self.Margin_point[0]
                                    else:
                                        end1 = self.Margin_point[j+1]

                                    if isIntersected(start,end,start1,end1):
                                        result = intersection_point(start,end,start1,end1)
                                        dis = (result.x - start.x)**2 + (result.y - start.y)**2
                                        line = (start1,end1,dis)
                                        tmp.append(line)

                                if tmp:
                                    tmp.sort(key = lambda x : x[2])
                                    for item in tmp:
                                        result = intersection_point(start,end,item[0],item[1])
                                        IsInside1 = self.figure.Accumulative(self.Margin,(start.x,start.y))
                                        result.get_in = get_in
                                        self.intersection_point.append(result)
                                        listpoint_inter.append(result)

                                        if not first_inter:
                                            first_inter = True
                                        if(get_in == 1):
                                            get_in = 0
                                        else:
                                            get_in = 1
                            
                            for i in range(len(self.Margin)):
                                first_inter = False
                                start = self.Margin_point[i]
                                Margin_inter.append(start)

                                if i == len(self.Margin_point) - 1:
                                    end = self.Margin_point[0]
                                else:
                                    end = self.Margin_point[i+1]
                                
                                tmp = []
                                for j in range(len(self.listpoint)):
                                    start1 = listpoint_point[j]
                                    if j == len(listpoint_point) - 1:
                                        end1 = listpoint_point[0]
                                    else:
                                        end1 = listpoint_point[j+1]

                                    if isIntersected(start,end,start1,end1):
                                        result = intersection_point(start1,end1,start,end)
                                        dis = (result.x - start.x)**2 + (result.y - start.y)**2
                                        line = (start1,end1,dis)
                                        tmp.append(line)

                                if tmp:
                                    tmp.sort(key = lambda x : x[2])
                                    for item in tmp:
                                        result = intersection_point(item[0],item[1],start,end,)
                                        index = FindPointIndex(listpoint_inter,result)

                                        Margin_inter.append(listpoint_inter[index])



                            Q = WA_Cutting(listpoint_inter,Margin_inter)
                            print("finished")
                            print("len_margin_inter = %d"%len(Margin_inter))
                            print("len_pointlist_inter = %d"%len(listpoint_inter))
                            # print("listpoint_inter:")
                            # for point in Margin_inter:
                            #     print("(%d,%d)"%(point.x,point.y))
                            #     if point.get_in == 1:
                            #         self.screen.set_at((point.x, point.y), ColorPicker("#FF0000"))
                            #     elif point.get_in == 0:
                            #         self.screen.set_at((point.x, point.y), ColorPicker("#0000FF"))
                            # print("margin_inter:")
                            # for point in Margin_inter:
                            #     print("(%d,%d)"%(point.x,point.y))
                            
                            # self.line.draw((Q[0].x,Q[0].y),(Q[1].x,Q[1].y),self.line.LineByE)

                            self.line.SetColor(ColorPicker("FF00000"))
                            
                            head = Q[0]
                            for i,point in enumerate(Q):
                                 
                                print("(%d,%d)"%(point.x,point.y))
                                start = point
                                    
                                if i == len(Q) -1:
                                    end = Q[0]
                                else:
                                    end = Q[i+1]
                                if end.x == INF or end.y == INF:
                                    self.line.draw((start.x,start.y),(head.x,head.y),self.line.LineByE)
                                    continue
                                if start.x == INF or start.y == INF:
                                    head = end
                                    continue

                                self.line.draw((start.x,start.y),(end.x,end.y),self.line.LineByE)


                    if self.drawing and event.pos[0] >=100:
                        finished = False
                        self.line.SetColor((0, 0, 0))
                        if self.figure==self.polygon:
                            if event.button==1 and not finished:
                                self.listpoint.append(event.pos)
                                listpoint_point.append(Point(event.pos[0],event.pos[1]))

                                if len(self.listpoint)>1:
                                    self.line.draw(self.listpoint[-2],self.listpoint[-1],self.line.DDA)
                            if finished:
                                finished = False
                            if event.button==3:
                                self.listpoint.append(event.pos)
                                listpoint_point.append(Point(event.pos[0],event.pos[1]))
                                self.line.draw(self.listpoint[-2],self.listpoint[-1],self.line.DDA)
                                self.line.draw(self.listpoint[-1],self.listpoint[0],self.line.DDA)
                                if not self.notfilling:
                                    self.figure.draw(self.listpoint)
                                    # self.figurelist.append(self.listpoint)
                                    self.listpoint=[]
                                finished = True

                        else:
                            if start != None and end == None:
                                end = event.pos
                            if start == None:
                                start = event.pos

                            if start != None and end != None:
                                self.figure.start = start
                                self.figure.end = end
                                # not sure whether it is needed
                                # self.figurelist.append(self.figure)
                                self.figure.draw(start,end,self.line.func)
                                start = None
                                end = None

                    # opreations in menu area
                    if event.pos[0] < 100:
                        # iretate the buttons to detect which line button was clicked
                        for button_ in button_list:
                            if button_.isOver():
                                self.figure = self.line
                                #set the algorithm
                                self.figure.func = button_dic[button_]
                                self.selected = True
                                self.drawing = True
                                # change the front_image to get it changed to indicate the status
                                button_.front_image = button_.imageDown
                                # change the status of the currently selected button
                                if self.selected_button:
                                    self.selected_button.selected = False
                                    self.selected_button.front_image = self.selected_button.imageUp
                                    self.selected_button = button_
                                    break
                                else:
                                    self.selected_button = button_

                        if button_Cir.isOver():
                            self.figure = self.circle
                            self.selected = True
                            self.drawing = True
                            button_Cir.fron_image = button_Cir.imageDown

                            if self.selected_button:
                                self.selected_button.selected = False
                                self.selected_button.front_image = self.selected_button.imageUp
                                self.selected_button = button_Cir
                                break
                            else:
                                self.selected_button = button_Cir
                        for button_ in button_fill_list:
                            if button_.isOver():
                                self.figure=self.polygon
                                self.figure.func=button_fill_dic[button_][0]
                                self.figure.IsInside=button_fill_dic[button_][1]
                                self.selected=True
                                self.drawing=True
                                self.notfilling = False
                                button_.front_image=button_.imageDown
                                if self.selected_button:
                                    self.selected_button.selected=False
                                    self.selected_button.front_image=self.selected_button.imageUp
                                    self.selected_button=button_
                                    break
                                else:
                                    self.selected_button=button_
                        if button_clear.isOver():
                            self.screen.fill((255,255,255))
                        if button_Polygon.isOver():
                            self.figure = self.polygon
                            self.drawing = True
                            self.notfilling = True

                        if button_Cutting.isOver():
                            self.selected = True
                            button_Cutting.front_image=button_Cutting.imageDown
                            if self.selected_button:
                                self.selected_button.selected=False
                                self.selected_button.front_image=self.selected_button.imageUp
                                self.selected_button=button_
                                break
                            else:
                                self.selected_button=button_
                            self.IsCutting = True
                            self.drawing = False




                elif event.type == MOUSEMOTION:
                    # self.brush.draw(event.pos)
                    pass

                elif event.type == KEYDOWN:
                    # Use key esc to clear screen
                    if event.key == K_ESCAPE:
                        self.screen.fill((255,255,255))
                        self.figurelist = []
                    #just 4 test
                    if event.key ==K_0:
                        self.screen.set_at((400,400),(0,0,0))

            # self.menu.draw()
            for button_ in button_list:
                button_.render()
            button_Cir.render()
            button_Cutting.render()
            #填充按钮
            for button_ in button_fill_list:
                button_.render()
            button_clear.render()
            button_Cutting.render()
            button_Polygon.render()
            pygame.display.update()


if __name__ == "__main__":
    app = Painter()
    app.run()
    # print(ColorPicker("#F2F2F2"))
