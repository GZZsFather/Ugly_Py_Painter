import pygame
from pygame.locals import *

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
            pygame.image.load("./icons/LBE.png").convert_alpha()
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
