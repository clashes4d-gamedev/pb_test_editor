import pygame
import SPRNVA as sprnva
from SPRNVA import Vector

class Sidebar:
    def __init__(self, win: pygame.Surface, pos: Vector, options: dict):
        self.win = win
        self.pos = pos
        self.size = Vector(self.win.get_width() - self.pos.x, self.win.get_height() - self.pos.y)
        self.options = options
        self.options_len = len(self.options)
        self.num_sub_options = len(self.options['OPTIONS'])
        self.option_height = int(self.size.y /self.options_len-1 + self.num_sub_options)
        print(self.option_height)
        self.collider = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.surf = pygame.Surface((self.collider.width, self.collider.height))

    def draw(self, bg_color=(64, 64, 64), test_color=(255, 255, 255)):
        self.surf.fill(bg_color)

        for index, section in enumerate(self.options):
            section_surf = pygame.Surface((self.surf.get_width(), self.option_height))
            section_surf.fill((25,25,25 + index))
            print(index, section)
            if index == 0:
                try:
                    sprnva.TextRenderer(section_surf, section_surf.get_width()/2, section_surf.get_height()/3, str(self.options['NAME']), 'Arial', 20, test_color)
                except KeyError:
                    sprnva.TextRenderer(section_surf, section_surf.get_width()/2, section_surf.get_height()/3, '', 'Arial', 20, test_color)

            if index == 1:
                try:
                    sprnva.TextRenderer(section_surf, section_surf.get_width()/2, section_surf.get_height()/3, str(self.options['DESCRIPTION']), 'Arial', 10, test_color)
                except KeyError:
                    sprnva.TextRenderer(section_surf, section_surf.get_width()/2, section_surf.get_height()/3, '', 'Arial', 10, test_color)

            #TODO Implement Options into Sidebar
            if index == 2:
                for i in self.options['OPTIONS']:
                    try:
                        sprnva.TextRenderer(section_surf, section_surf.get_width()/2, section_surf.get_height()/3, str(self.options['OPTIONS'][str(i)]['NAME']), 'Arial', 20, test_color)
                    except KeyError:
                        sprnva.TextRenderer(section_surf, section_surf.get_width()/2, section_surf.get_height()/3, '', 'Arial', 10, test_color)

            self.surf.blit(section_surf, (0, index * self.option_height))
        self.win.blit(self.surf, (self.collider.x, self.collider.y))
