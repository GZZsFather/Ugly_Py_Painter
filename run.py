
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
        # self.menu = Menu(self.screen)
        self.drawing = False
        self.figure = self.line
        self.selected_button = None


    def run(self):
        self.screen.fill((255,255,255))
        start = None
        end = None

        button_DDA = Button("./icons/DDA.png","./icons/MPL.png",(50,50),self.screen)
        button_BRE = Button("./icons/BRE.png","./icons/MPL.png",(50,70),self.screen)
        button_LBE = Button("./icons/LBE.png","./icons/MPL.png",(50,90),self.screen)
        button_MPL = Button("./icons/MPL.png","./icons/MPL.png",(50,110),self.screen)
        button_Cir = Button("./icons/Cir.png","./icons/MPL.png",(50,130),self.screen)

        # a list to iterate the buttons
        button_list = [button_DDA,button_BRE,button_LBE,button_MPL]
        # dictation for selecting algorithm
        button_dic = {button_DDA:self.figure.DDA, button_BRE:self.figure.bresenhamline, button_LBE:self.figure.LineByE,button_MPL:self.figure.MidPointLine,}


        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

                elif event.type == MOUSEBUTTONUP:
                    # self.brush.end_draw()
                    pass

                elif event.type == MOUSEBUTTONDOWN:
                    if self.drawing and event.pos[0] >=100:
                        if start != None and end == None:
                            end = event.pos
                        if start == None:
                            start = event.pos

                        if start != None and end != None:
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


                elif event.type == MOUSEMOTION:
                    # self.brush.draw(event.pos)
                    pass

                elif event.type == KEYDOWN:
                    # Use key esc to clear screen
                    if event.key == K_ESCAPE:
                        self.screen.fill((255,255,255))
                    #just 4 test
                    if event.key ==K_0:
                        self.screen.set_at((400,400),(0,0,0))

            # self.menu.draw()
            for button_ in button_list:
                button_.render()
            # button_DDA.render()
            # button_BRE.render()
            # button_LBE.render()
            # button_MPL.render()
            button_Cir.render()

            pygame.display.update()


if __name__ == "__main__":
    app = Painter()
    app.run()
    # print(ColorPicker("#F2F2F2"))
