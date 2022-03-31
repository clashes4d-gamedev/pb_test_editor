from re import T
import pygame
from sys import exit
import os
import SPRNVA as sprnva
import time
from SPRNVA import Vector
pygame.init()

# TODO Optimize
# TODO just implement saving the file to a .lvl file and this project is done.
class Main:
    def __init__(self):
        # Sets the window size to be the resolution of the monitor
        self.info_object = pygame.display.Info()
        self.win_size = (self.info_object.current_w, self.info_object.current_h)
        # Finds the center coordinates of the screen and stores them in a Vector
        self.center = Vector(self.win_size[0] / 2, self.win_size[1] / 2)

        # Actual window setup
        self.win = pygame.display.set_mode(self.win_size, pygame.FULLSCREEN, vsync=1)
                                    # TODO REPLACE WITH PROJECT NAME
        pygame.display.set_caption('PB LEVEL EDITOR')
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Button setup and tile type selection
        self.tile_select_b_size = Vector(50, 50)
        self.tile_types = {'1': 'NONE / Air', '2': 'stone', '3': 'wood'}
        self.current_selected_tile_type = '1'

        # Stores the 'Drawn' tiles in a list
        self.tiles = []
        self.tile_m_x = 0
        self.tile_m_y = 0
        self.selected_tile = Vector(0, 0)

        # Checks if the user has pressed the export button
        self.export = False

        # Stores the Grid dimensions and tile size in a list
        self.grid_params = {'x': '0', 'y': '0', 'size': '0'}

    def update(self):
        grid_surf = pygame.Surface((self.win_size[0]/1.2, self.win_size[1]/1.2))
        gen_map = True

        grid_param_inputs = {}
        for i, key in enumerate(self.grid_params):
            grid_param_inputs[key] = sprnva.InputBox(self.win, Vector(self.center.x/2, (self.center.y*2 - 60) + i*20), Vector(50, 20))

        while True:
            # Clears surfaces
            grid_surf.fill((64, 64, 64))
            grid_rect = grid_surf.get_rect()
            self.win.fill((0, 0, 0))

            # Displays fps
            sprnva.TextRenderer(self.win, self.win_size[0] - 150, 50, 'FPS: ' + str(int(self.clock.get_fps())), 'Arial', 20, (255, 0, 0))

            # Get's events
            events = pygame.event.get()

            # Get's keys currently pressed and the mouse position and buttons which are pressed.
            keys = pygame.key.get_pressed()
            m_x, m_y = pygame.mouse.get_pos()
            m_btns = pygame.mouse.get_pressed()

            # Checks if Escape has been pressed, if so exit
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                print(self.tiles)
                exit()

            # Sets up the export button
            ex_button = sprnva.Button(self.win,
                                           self.win_size[0] - 120,
                                           self.center.y,
                                           100,
                                           50,
                                           (m_x, m_y),
                                           m_btns,
                                           0, btn_text='Export as .lvl')

            # loop through available tile types and generate a button at the button of the screen if the button is pressed the active tile type switches, default is the first dictonary entry
            for i, (key, value) in enumerate(self.tile_types.items()):
                sel_btn = sprnva.Button(self.win,
                                        i*self.tile_select_b_size.x + self.center.x - (self.tile_select_b_size.x * len(self.tile_types)/2),
                                        self.center.y*2 - self.tile_select_b_size.y,
                                        self.tile_select_b_size.x,
                                        self.tile_select_b_size.y,
                                        (m_x, m_y),
                                        m_btns,
                                        0, btn_text=value)
                is_pressed = sel_btn.draw()

                if is_pressed is True:
                    self.current_selected_tile_type = str(key)

            # Draws a text which tells the user what tile he has currently selected.
            sprnva.TextRenderer(self.win, self.tile_select_b_size.x + self.center.x - (self.tile_select_b_size.x * len(self.tile_types))/2 + self.tile_select_b_size.x/2, self.center.y*2 - self.tile_select_b_size.y - 20, 'Current selected tile type: ' + self.tile_types[self.current_selected_tile_type], 'Arial', 10, (255, 255, 255))

            # Draws and gets the input value out of the three text boxes at the bottom of the screen.
            for index, key in enumerate(grid_param_inputs):
                sprnva.TextRenderer(self.win, grid_param_inputs[key].collider.x - 64, grid_param_inputs[key].collider.y + 10, 'Grid ' + key + ':', 'Arial', 16, (255, 255, 255))
                grid_param_inputs[key].get_input(events)
                grid_param_inputs[key].update((True, False, False))
                grid_param_inputs[key].draw()
                try:
                    self.grid_params[key] = int(grid_param_inputs[key].get_value())
                except ValueError:
                    self.grid_params[key] = 0

            # Draws a Grid in given dimensions. and generates tile coordinates
            try:
                self.tile_m_x = m_x // int(self.grid_params['size']) * int(self.grid_params['size'])
                self.tile_m_y = m_y // int(self.grid_params['size']) * int(self.grid_params['size'])

                sprnva.TextRenderer(self.win, self.win_size[0] - 150, 80, f'POS: {self.tile_m_x / int(self.grid_params["size"])+1, self.tile_m_y / int(self.grid_params["size"])+1}', 'Arial', 20, (255, 255, 255))

                pygame.draw.rect(grid_surf, (255, 255, 255), pygame.Rect(self.tile_m_x, self.tile_m_y, int(self.grid_params['size']), int(self.grid_params['size'])))

                if self.grid_params['x'] != '0' and self.grid_params['y'] != '0' and self.grid_params['size'] != '0' and gen_map is True:
                    row = int(self.grid_params['x']) * ['0']
                    self.tiles = int(self.grid_params['y']) * [row]
                    gen_map = False

                # Generates grid
                for y in range(int(self.grid_params['y'])+1):
                    if int(self.grid_params['y']) <= grid_rect.height:
                        if y == int(self.grid_params['y']):
                            pygame.draw.line(grid_surf, (255, 0, 0), (0, y * int(self.grid_params['size'])), (int(self.grid_params['size']) * int(self.grid_params['x']), y * int(self.grid_params['size'])))
                        else:
                            pygame.draw.line(grid_surf, (255, 255, 255), (0, y * int(self.grid_params['size'])), (int(self.grid_params['size']) * int(self.grid_params['x']), y * int(self.grid_params['size'])))

                    for x in range(int(self.grid_params['x'])+1):
                        if int(self.grid_params['x']) <= grid_rect.width:
                            if x == int(self.grid_params['x']):
                                pygame.draw.line(grid_surf, (255, 0, 0), (x * int(self.grid_params['size']), 0), (x * int(self.grid_params['size']), int(self.grid_params['size']) * y))
                            else:
                                pygame.draw.line(grid_surf, (255, 255, 255), (x * int(self.grid_params['size']), 0), (x * int(self.grid_params['size']), int(self.grid_params['size']) * y))

                got_x = False
                got_y = False

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for y, row in enumerate(self.tiles):
                                for x, tile in enumerate(row):
                                    if grid_rect.collidepoint(m_x, m_y):
                                        if y == self.tile_m_y//int(self.grid_params['size']) and got_y == False:
                                            if x == self.tile_m_x//int(self.grid_params['size']) and got_x == False:
                                                self.tiles[y][x] = self.current_selected_tile_type

                    else:
                        got_x = False
                        got_y = False

                if self.grid_params['x'] != '0' and self.grid_params['y'] != '0' and self.grid_params['size'] != '0':
                    self.export = ex_button.draw()


            except ZeroDivisionError:
                pass


            if self.export:
                ex_surf = pygame.Surface((self.win_size[0], self.win_size[1]))
                ex_surf_rect = ex_surf.get_rect()
                tb_ex_path = sprnva.InputBox(ex_surf, Vector(20, ex_surf_rect.height / 2 - 10), Vector(ex_surf_rect.width - 40, 20))
                self.win.fill((0,0,0))
                while True:
                    ex_surf.fill((64, 64, 64))
                    # Displays fps
                    sprnva.TextRenderer(ex_surf, self.win_size[0] - 150, 50, 'FPS: ' + str(int(self.clock.get_fps())),
                                        'Arial', 20, (255, 0, 0))

                    events = pygame.event.get()

                    keys = pygame.key.get_pressed()
                    m_x, m_y = pygame.mouse.get_pos()
                    m_btns = pygame.mouse.get_pressed()

                    sprnva.TextRenderer(ex_surf,
                                        ex_surf_rect.centerx,
                                        ex_surf_rect.centery - ex_surf_rect.height/2 + 40,
                                        'Enter Export path: ', 'Arial', 20, (255, 255, 255))

                    export_button = sprnva.Button(ex_surf,
                                  ex_surf_rect.width - 120,
                                  ex_surf_rect.height - 70,
                                  100,
                                  50,
                                  (m_x, m_y),
                                  m_btns,
                                  0, btn_text='Export as .lvl')

                    back_button = sprnva.Button(ex_surf,
                                                  20,
                                                  ex_surf_rect.height - 70,
                                                  100,
                                                  50,
                                                  (m_x, m_y),
                                                  m_btns,
                                                  0, btn_text='Back')

                    tb_ex_path.get_input(events)
                    tb_ex_path.update((True, False, False))
                    tb_ex_path.draw(color=(255, 255, 255), text_color=(0, 0, 0))

                    back_off = back_button.draw()
                    should_export = export_button.draw()

                    if should_export:
                        ex_path = tb_ex_path.get_value()
                        file = open(ex_path + '.lvl', 'w')
                        lines = []

                        for row in self.tiles:
                            for char in row:
                                lines.append(char)
                            lines.append('\n')

                        print(lines)
                        file.writelines(lines)
                        file.close()
                        pygame.quit()
                        exit()

                    if back_off:
                        break

                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            print(self.tiles)
                            exit()

                    if keys[pygame.K_ESCAPE]:
                        pygame.quit()
                        exit()

                    self.win.blit(ex_surf, (0, 0))
                    pygame.display.update()
                    self.clock.tick(self.fps)

            # Handel's exit
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            for r_index, row in enumerate(self.tiles):
                for c_index, char in enumerate(row):
                    if char == '1':
                        pygame.draw.rect(grid_surf, (255, 0, 0), pygame.Rect(c_index * int(self.grid_params['size']),
                                                                             r_index * int(self.grid_params['size']),
                                                                             int(self.grid_params['size']),
                                                                             int(self.grid_params['size'])))


            # Draws, resets the loop and keeps the framerate capped.
            self.win.blit(grid_surf, (0, 0))
            pygame.display.update()
            self.clock.tick(self.fps)


# calls main script.
if __name__ == '__main__':
    Main().update()
