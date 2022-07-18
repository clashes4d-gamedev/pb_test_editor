import pygame
import SPRNVA as sprnva
import json
from sys import exit
from pygame import gfxdraw
from SPRNVA import Vector2D
from pandas import DataFrame

pygame.init()


# TODO Optimize
# TODO Find a way to embed image textures
class Main:
    def __init__(self):
        # Sets the window size to be the resolution of the monitor
        self.info_object = pygame.display.Info()
        self.win_size = (self.info_object.current_w, self.info_object.current_h)

        # Finds the center coordinates of the screen and stores them in a Vector2D
        self.center = Vector2D(self.win_size[0] / 2, self.win_size[1] / 2)

        # Actual window setup
        self.win = pygame.display.set_mode(self.win_size, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Handeling events
        self.keys = pygame.key.get_pressed()
        self.m_x, self.m_y = pygame.mouse.get_pos()
        self.m_btns = pygame.mouse.get_pressed()
        self.offset_vec = Vector2D(0, 0)
        self.current_offset = Vector2D(0, 0)
        self.m_vec = Vector2D(0, 0)
        self.org_vec = Vector2D(0, 0)

        # Button setup and tile type selection
        self.tile_select_b_size = Vector2D(50, 50)
        self.tile_types = open('config.json')
        self.tile_types = json.load(self.tile_types)
        self.tile_types = self.tile_types['tile_types']
        self.current_selected_tile_type = '1'

        # Stores the 'Drawn' tiles in a dict
        self.tiles = DataFrame(list())
        self.tiles = self.tiles.to_dict()
        self.tile_m_x = 0
        self.tile_m_y = 0
        self.selected_tile = Vector2D(0, 0)

        # Checks if the user has pressed the export button
        self.export = False

        # Stores the Grid dimensions and tile size in a dict
        self.grid_params = {'x': '0', 'y': '0', 'size': '0'}

    def grid_param_input_fields(self, events, grid_param_inputs):
        # Draws and gets the input value out of the three text boxes at the bottom of the screen.
        # TODO Make the x and y display correctly
        for index, key in enumerate(grid_param_inputs):
            sprnva.TextRenderer(self.win, grid_param_inputs[key].collider.x - 64,
                                grid_param_inputs[key].collider.y + 10, 'Grid ' + key + ':', 'Arial', 16,
                                (255, 255, 255)).draw()

            grid_param_inputs[key].update(events)
            grid_param_inputs[key].draw()
            try:
                self.grid_params[key] = int(grid_param_inputs[key].get_value())
            except ValueError:
                self.grid_params[key] = 0

    def export_screen(self):
        ex_surf = pygame.Surface((self.win_size[0], self.win_size[1]))
        ex_surf_rect = ex_surf.get_rect()
        tb_ex_path = sprnva.InputBox(ex_surf, Vector2D(20, ex_surf_rect.height / 2 - 10),
                                     Vector2D(ex_surf_rect.width - 40, 20))
        while True:
            self.win.fill((0, 0, 0))
            ex_surf.fill((64, 64, 64))
            # Displays fps
            sprnva.TextRenderer(ex_surf, self.win_size[0] - 150, 50, 'FPS: ' + str(int(self.clock.get_fps())), 'Arial',
                                20, (255, 0, 0)).draw()

            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            m_x, m_y = pygame.mouse.get_pos()

            sprnva.TextRenderer(ex_surf, ex_surf_rect.centerx, ex_surf_rect.centery - ex_surf_rect.height / 2 + 40,
                                'Enter Export path: ', 'Arial', 20, (255, 255, 255)).draw()

            export_button = sprnva.Button(ex_surf, ex_surf_rect.width - 120, ex_surf_rect.height - 70,
                                          100, 50, (54, 54, 54), text='Export as .lvl')

            back_button = sprnva.Button(ex_surf, 20, ex_surf_rect.height - 70, 100, 50, (54, 54, 54), text='Back')

            tb_ex_path.update(events)
            tb_ex_path.draw()

            back_button.draw()
            export_button.draw()

            back_off = back_button.get_state()
            should_export = export_button.get_state()

            if should_export:
                # .lvl Encoder/file generator
                ex_path = tb_ex_path.get_value()
                file = open(ex_path + '.lvl', 'w')
                tile_lines = []
                for row in self.tiles.items():
                    tile_line = []
                    for tile in row[1].items():
                        tile_line.append(tile[1])
                    tile_lines.append(tile_line)

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
            # Draws the virtual cursor
            pygame.draw.circle(self.win, (255, 255, 255), (m_x, m_y), 3)
            pygame.draw.circle(self.win, (0, 0, 0), (self.m_x, self.m_y), 3, width=1)

            pygame.display.update()
            self.clock.tick(self.fps)

    def update(self):
        grid_surf = pygame.Surface((self.win_size[0], self.win_size[1] / 1.2))
        gen_map = True
        lock_m_pos = False

        grid_param_inputs = {}
        for i, key in enumerate(self.grid_params):
            grid_param_inputs[key] = sprnva.InputBox(self.win,
                                                     Vector2D(self.center.x / 2, (self.center.y * 2 - 80) + i * 20),
                                                     Vector2D(50, 20))

        while True:
            # Clears surfaces
            grid_surf.fill((64, 64, 64))
            grid_rect = grid_surf.get_rect()
            self.win.fill((0, 0, 0))

            self.current_offset += -self.offset_vec

            # Displays fps
            sprnva.TextRenderer(self.win, self.win_size[0] - 50, self.win_size[1] - 150,
                                'FPS: ' + str(int(self.clock.get_fps())), 'Arial', 20, (255, 0, 0)).draw()

            # Get's events
            events = pygame.event.get()

            # Get's keys currently pressed and the mouse position and buttons which are pressed.
            self.keys = pygame.key.get_pressed()
            self.m_x, self.m_y = pygame.mouse.get_pos()
            self.m_btns = pygame.mouse.get_pressed()

            # This gets the offset the mouse has traveled if mouse 2 is pressed and the mouse has moved
            # TODO Optimize this write this in a function!
            if self.m_btns[2]:
                if lock_m_pos is False:
                    origin_m_x = self.m_x
                    origin_m_y = self.m_y
                    lock_m_pos = True

                if lock_m_pos:
                    self.m_vec = Vector2D(self.m_x, self.m_y)
                    self.org_vec = Vector2D(origin_m_x, origin_m_y)
            else:
                self.offset_vec = Vector2D(0, 0)

            # Handel's events
            for event in events:
                # handel's exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Handel's mouseevents
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.offset_vec = self.org_vec - self.m_vec
                        lock_m_pos = False

            # Checks if Escape has been pressed, if so exit
            if self.keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

            # Sets up the export button
            ex_button = sprnva.Button(self.win,
                                      self.win_size[0] - 120,
                                      self.win_size[1] - 100,
                                      100,
                                      50,
                                      (50, 50, 50),
                                      text='Export as .lvl')

            # Draws a text which tells the user what tile he has currently selected.
            sprnva.TextRenderer(self.win, self.tile_select_b_size.x + self.center.x - (
                self.tile_select_b_size.x * len(self.tile_types)) / 2 + self.tile_select_b_size.x / 2,
                                self.center.y * 2 - self.tile_select_b_size.y - 40,
                                'Current selected tile type: ' + self.tile_types[self.current_selected_tile_type][
                                    'name'],
                                'Arial', 10, (255, 255, 255)).draw()

            for tile in self.tile_types:
                tile_name = self.tile_types[tile]['name']

                sel_btn = sprnva.Button(self.win,
                                        int(tile) * self.tile_select_b_size.x + self.center.x - (
                                            self.tile_select_b_size.x * len(self.tile_types) / 2),
                                        self.center.y * 2 - self.tile_select_b_size.y - 20,
                                        self.tile_select_b_size.x,
                                        self.tile_select_b_size.y,
                                        (54, 54, 54),
                                        text=tile_name)

                sel_btn.draw()
                is_pressed = sel_btn.get_state()

                if is_pressed is True:
                    self.current_selected_tile_type = str(tile)

            # Generates the input fields for the grid parameter
            self.grid_param_input_fields(events, grid_param_inputs)

            # Draws a Grid in given dimensions. and generates tile coordinates
            try:
                # Tile coordinates
                self.tile_m_x = self.m_x // int(self.grid_params['size']) * int(
                    self.grid_params['size'])  # + self.current_offset.x
                self.tile_m_y = self.m_y // int(self.grid_params['size']) * int(
                    self.grid_params['size'])  # + self.current_offset.y

                if self.grid_params['x'] != '0' and self.grid_params['y'] != '0' and self.grid_params[
                    'size'] != '0' and gen_map is True:
                    row = int(self.grid_params['x']) * ['0']
                    self.tiles = int(self.grid_params['y']) * [row]
                    self.tiles = DataFrame(self.tiles)
                    self.tiles = self.tiles.to_dict()
                    gen_map = False

                if self.grid_params['x'] != '0' and self.grid_params['y'] != '0' and self.grid_params['size'] != '0':
                    ex_button.draw()
                    self.export = ex_button.get_state()

                # print(self.current_offset.x//int(self.grid_params['size']), self.current_offset.y//int(self.grid_params['size']))

                # THIS FUCKING WORKS YEEEEEEEEEEEEEE AND IT DOESNT USE PANDAS DATAFRAMES! so i basically doubled the framerate. this is x77 times faster then using iterrows()
                x = 0
                y = 0
                for row in self.tiles.items():
                    x = 0
                    for tile in row[1].items():
                        # Generates grid
                        gfxdraw.pixel(grid_surf, x * int(self.grid_params['size']) + self.current_offset.x,
                                      y * int(self.grid_params['size']) + self.current_offset.y, (255, 255, 255))

                        if grid_rect.collidepoint(self.m_x, self.m_y):
                            if self.m_btns[0]:
                                if x == (self.tile_m_x // int(self.grid_params['size']) - round(
                                    self.current_offset.x / int(self.grid_params['size']))) and y == (
                                    self.tile_m_y // int(self.grid_params['size']) - round(
                                    self.current_offset.y / int(self.grid_params['size']))):
                                    self.tiles[y][x] = self.current_selected_tile_type

                        if tile[1] in self.tile_types:
                            for key in self.tile_types:
                                if tile[1] == key:
                                    pygame.draw.rect(grid_surf, (
                                        (self.tile_types[tile[1]]['color'][0], self.tile_types[tile[1]]['color'][1], self.tile_types[tile[1]]['color'][2])),
                                                     pygame.Rect(
                                                         x * int(self.grid_params['size']) + 1 + self.current_offset.x,
                                                         y * int(self.grid_params['size']) + 1 + self.current_offset.y,
                                                         int(self.grid_params['size']) - 1,
                                                         int(self.grid_params['size']) - 1))
                        x += 1
                    y += 1

                # Draws the tile cursor at the given tile
                if grid_rect.collidepoint(self.m_x, self.m_y):
                    # Tells the user the position of the current tile he is hovering over.
                    sprnva.TextRenderer(self.win, self.win_size[0] - 250, self.win_size[1] - 50,
                                        f'POS: {self.tile_m_x // int(self.grid_params["size"]) - round(self.current_offset.x / int(self.grid_params["size"])) + 1, self.tile_m_y // int(self.grid_params["size"]) - round(self.current_offset.y / int(self.grid_params["size"])) + 1}',
                                        'Arial', 20, (255, 255, 255)).draw()

            except ZeroDivisionError:
                self.tiles = DataFrame(list())
                self.tile = self.tiles.to_dict()
                gen_map = True

            # If the tilesize is 0 a ZeroDivisionError will be triggered and the Tilemap resets.
            sprnva.TextRenderer(self.win, 200, self.win_size[1] - 50, 'Set the Tilesize to 0 to reset the map.',
                                'Arial', 20, (255, 255, 255)).draw()

            # Handel's the export screen
            if self.export:
                # TODO This is only a temporary solution to use just a delay
                pygame.time.delay(1000)
                self.export_screen()

            # Draws, resets the loop and keeps the framerate capped.
            self.win.blit(grid_surf, (0, 0))

            # Draws the virtual cursor
            # pygame.draw.circle(self.win, (255, 255, 255), (self.m_x, self.m_y), 3)
            # pygame.draw.circle(self.win, (0, 0, 0), (self.m_x, self.m_y), 3, width=1)

            pygame.display.flip()
            self.clock.tick(self.fps)


# calls main script.
if __name__ == '__main__':
    Main().update()
