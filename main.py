# This programm is so janky i just dont know how it even works. :)
import pygame
import SPRNVA as sprnva
import json
from sys import exit
from SPRNVA import Vector
from pandas import DataFrame
pygame.init()

# TODO Optimize
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
        self.tile_types = open('config.json')
        self.tile_types = json.load(self.tile_types)
        self.tile_types = self.tile_types['tile_types']
        self.current_selected_tile_type = '1'

        # Stores the 'Drawn' tiles in a list
        self.tiles = DataFrame(list())
        self.tile_m_x = 0
        self.tile_m_y = 0
        self.selected_tile = Vector(0, 0)
        self.image_tiles = {}
        self.load_image_tiles = True

        #Checks if the tile is an image if so store the image path in a python dictionary
        for tile_index in self.tile_types:
            if self.tile_types[tile_index]['file_path'] != str():
                self.image_tiles[tile_index] = self.tile_types[tile_index]['file_path']
            else:
                self.image_tiles[tile_index] = str()

        print(self.image_tiles)

        # Checks if the user has pressed the export button
        self.export = False

        # Stores the Grid dimensions and tile size in a dict
        self.grid_params = {'x': '0', 'y': '0', 'size': '0'}

    def grid_param_input_fields(self, events, grid_param_inputs):
        # Draws a text which tells the user what tile he has currently selected.
        sprnva.TextRenderer(self.win, self.tile_select_b_size.x + self.center.x - (self.tile_select_b_size.x * len(self.tile_types))/2 + self.tile_select_b_size.x/2, self.center.y*2 - self.tile_select_b_size.y - 20, 'Current selected tile type: ' + self.tile_types[self.current_selected_tile_type]['name'], 'Arial', 10, (255, 255, 255))

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

    def export_screen(self):
        ex_surf = pygame.Surface((self.win_size[0], self.win_size[1]))
        ex_surf_rect = ex_surf.get_rect()
        tb_ex_path = sprnva.InputBox(ex_surf, Vector(20, ex_surf_rect.height / 2 - 10), Vector(ex_surf_rect.width - 40, 20))
        while True:
            self.win.fill((0,0,0))
            ex_surf.fill((64, 64, 64))
            # Displays fps
            sprnva.TextRenderer(ex_surf, self.win_size[0] - 150, 50, 'FPS: ' + str(int(self.clock.get_fps())), 'Arial', 20, (255, 0, 0))

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
                # .lvl Encoder/file generator
                ex_path = tb_ex_path.get_value()
                file = open(ex_path + '.lvl', 'w')
                transposed_tiles = self.tiles.transpose()
                tile_lines = transposed_tiles.values.tolist()

                file.write('TILE_TYPES_BEGIN\n')
                
                file.write(f'{self.tile_types}\n')

                file.write('TILE_TYPES_END\n')

                file.write('\n')

                file.write('TILE_SIZE_BEGIN\n')
                file.write(f'{self.grid_params["size"]}\n')
                file.write('TILE_SIZE_END\n')

                file.write('\n')

                file.write('LAYOUT_BEGIN\n')

                for row in tile_lines:
                    for col in row:
                        file.write(str(col))
                    file.write('\n')

                file.write('LAYOUT_END\n')

                file.close()
                pygame.quit()
                exit()

            if back_off:
                break

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

            self.win.blit(ex_surf, (0, 0))
            pygame.display.update()
            self.clock.tick(self.fps)

    def update(self):
        grid_surf = pygame.Surface((self.win_size[0], self.win_size[1]/1.2))
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
            sprnva.TextRenderer(self.win, self.win_size[0] - 50, self.win_size[1] - 150, 'FPS: ' + str(int(self.clock.get_fps())), 'Arial', 20, (255, 0, 0))

            # Get's events
            events = pygame.event.get()

            # Get's keys currently pressed and the mouse position and buttons which are pressed.
            keys = pygame.key.get_pressed()
            m_x, m_y = pygame.mouse.get_pos()
            m_btns = pygame.mouse.get_pressed()

            # Checks if Escape has been pressed, if so exit
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

            # Sets up the export button
            ex_button = sprnva.Button(self.win,
                                           self.win_size[0] - 120,
                                           self.win_size[1] - 100,
                                           100,
                                           50,
                                           (m_x, m_y),
                                           m_btns,
                                           0, btn_text='Export as .lvl')

            for tile in self.tile_types:
                tile_name = self.tile_types[tile]['name']

                sel_btn = sprnva.Button(self.win,
                                        int(tile)*self.tile_select_b_size.x + self.center.x - (self.tile_select_b_size.x * len(self.tile_types)/2),
                                        self.center.y*2 - self.tile_select_b_size.y,
                                        self.tile_select_b_size.x,
                                        self.tile_select_b_size.y,
                                        (m_x, m_y),
                                        m_btns,
                                        0, btn_text=tile_name)

                is_pressed = sel_btn.draw()

                if is_pressed is True:
                    self.current_selected_tile_type = str(tile)

            # Generates the input fields for the grid parameter
            self.grid_param_input_fields(events, grid_param_inputs)

            # Draws a Grid in given dimensions. and generates tile coordinates
            try:
                # Tile coordinates
                self.tile_m_x = m_x // int(self.grid_params['size']) * int(self.grid_params['size'])
                self.tile_m_y = m_y // int(self.grid_params['size']) * int(self.grid_params['size'])

                # Tells the user the position of the current tile he is hovering over.
                sprnva.TextRenderer(self.win, self.win_size[0] - 250, self.win_size[1] - 50, f'POS: {self.tile_m_x / int(self.grid_params["size"])+1, self.tile_m_y / int(self.grid_params["size"])+1}', 'Arial', 20, (255, 255, 255))

                # Draws the tile cursor at the given tile
                pygame.draw.rect(grid_surf, (255, 255, 255), pygame.Rect(self.tile_m_x, self.tile_m_y, int(self.grid_params['size']), int(self.grid_params['size'])))

                # Get's the grid parameters and draws the export button if they are not zero
                if self.grid_params['x'] != '0' and self.grid_params['y'] != '0' and self.grid_params['size'] != '0' and gen_map is True:
                    row = int(self.grid_params['x']) * ['0']
                    self.tiles = int(self.grid_params['y']) * [row]
                    self.tiles = DataFrame(self.tiles)
                    gen_map = False

                if self.grid_params['x'] != '0' and self.grid_params['y'] != '0' and self.grid_params['size'] != '0':
                    self.export = ex_button.draw()

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

                # (This worked, ty stackoverflow) Checks if mousebutton is pressed above tile and replace tile with currently selected tile
                if grid_rect.collidepoint(m_x, m_y):
                    y = 0
                    x = 0
                    for row in self.tiles.iterrows():
                        x = 0
                        for col in self.tiles:
                            if x == self.tile_m_x/int(self.grid_params['size']) and y == self.tile_m_y/int(self.grid_params['size']):
                                if m_btns[0]:
                                    self.tiles.loc[x, y] = self.current_selected_tile_type

                            x += 1
                        y += 1
                else:
                    pass

            except ZeroDivisionError:
                self.tiles = DataFrame(list())
                gen_map = True

            # If the tilesize is 0 a ZeroDivisionError will be triggered and the Tilemap resets.
            sprnva.TextRenderer(self.win, 200, self.win_size[1] - 50, 'Set the Tilesize to 0 to reset the map.', 'Arial', 20, (255, 255, 255))

            # Handel's the export screen
            if self.export:
                #TODO This is only a temporary solution
                pygame.time.delay(1000)
                self.export_screen()

            # Handel's exit
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Draws the tile types at the correct location
            y = 0
            x = 0
            for row in self.tiles.iterrows():
                x = 0
                for col in self.tiles:
                    for tile_index in self.tile_types:
                        if self.tiles.loc[x, y] == tile_index:
                            if tile_index != '0':
                                pygame.draw.rect(grid_surf, (self.tile_types[tile_index]['alt_r'], self.tile_types[tile_index]['alt_g'], self.tile_types[tile_index]['alt_b']),
                                        pygame.Rect(
                                        x * int(self.grid_params['size']),
                                        y * int(self.grid_params['size']),
                                        int(self.grid_params['size']),
                                        int(self.grid_params['size'])))
                    x += 1
                y += 1

            # Draws, resets the loop and keeps the framerate capped.
            self.win.blit(grid_surf, (0, 0))
            pygame.display.update()
            self.clock.tick(self.fps)

# calls main script.
if __name__ == '__main__':
    Main().update()
