import pygame
from sys import exit
import SPRNVA as sprnva
from SPRNVA import Vector
from lib.sidebar import Sidebar

pygame.init()

class Main:
    def __init__(self):
        self.info_object = pygame.display.Info()
        self.win_size = (self.info_object.current_w, self.info_object.current_h)
        self.center = Vector(self.win_size[0]/2, self.win_size[1]/2)
        self.win = pygame.display.set_mode(self.win_size, pygame.NOFRAME, vsync=1)
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.options = {'NAME': 'SAMPLE TEXT',
                        'DESCRIPTION': 'SOME DESCRIPTION OF OBJECT.',
                        'OPTIONS': {'1': {'NAME': 'OPTION_1',
                                         'DESCRIPTION': 'description of option_1',
                                         'TYPE': 'TEXTBOX',
                                         'RETURNTYPE': str()},
                                    '2': {'NAME': 'OPTION_2',
                                          'DESCRIPTION': 'description of option_2',
                                          'TYPE': 'BUTTON',
                                          'RETURNTYPE': bool()}
                                    }
                        }
        self.sidebar = Sidebar(self.win, Vector(self.center.x + self.center.x/4, 0), self.options)
        #self.text_box = sprnva.InputBox(self.win, self.center, Vector(50, 25))

    def update(self):
        while True:
            self.win.fill((0, 0, 0))
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                #self.text_box.get_input(event)

            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

            #self.text_box.update((True, False, False))
            #self.text_box.draw()
            self.sidebar.draw()

            pygame.display.update()
            self.clock.tick(self.fps)

if __name__ == '__main__':
    Main().update()