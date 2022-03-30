import pygame
from sys import exit
import SPRNVA as sprnva
from SPRNVA import Vector
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
        self.tile_types = {'1': 'grass', '2': 'stone', '3': 'wood'}
        self.current_selected_tile_type = '1'

        # Stores the 'Drawn' tiles in a list
        self.tiles = []
        self.tile_m_x = 0
        self.tile_m_y = 0

        # Stores the Grid dimensions and tile size in a list
        self.grid_params = {'x': '0', 'y': '0', 'size': '2'}

    def update(self):
        grid_surf = pygame.Surface((self.win_size[0]/1.2, self.win_size[1]/1.2))
        grid_rect = grid_surf.get_rect()

        grid_param_inputs = {}
        for i, key in enumerate(self.grid_params):
            grid_param_inputs[key] = sprnva.InputBox(self.win, Vector(self.center.x/2, (self.center.y*2 - 60) + i*20), Vector(50, 20))

        while True:
            # Clears surfaces
            grid_surf.fill((64, 64, 64))
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
                exit()

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
                sprnva.TextRenderer(self.win, grid_param_inputs[key].collider.x - 64, grid_param_inputs[key].collider.y + 10, 'Grid length ' + key + ':', 'Arial', 16, (255, 255, 255))
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

                pygame.draw.rect(grid_surf, (255, 255, 255), pygame.Rect(self.tile_m_x, self.tile_m_y, int(self.grid_params['size']), int(self.grid_params['size'])))

                for y in range(int(int(self.grid_params['y']) / int(self.grid_params['size']))):
                    pygame.draw.line(grid_surf, (255, 255, 255), (0, int(self.grid_params['size']) * y), (int(self.grid_params['x']), int(self.grid_params['size']) * y))

                    for x in range(int(int(self.grid_params['x']) / int(self.grid_params['size']))):
                        pygame.draw.line(grid_surf, (255, 255, 255), (int(self.grid_params['size']) * x, 0), (int(self.grid_params['size']) * x, int(self.grid_params['y'])))

                if m_btns == (True, False, False):
                    row = int(self.tile_m_x/int(self.grid_params['size'])) * '0'
                    self.list = int(self.tile_m_y/int(self.grid_params['size'])) * row
                    print(int(self.tile_m_x/int(self.grid_params['size'])), int(self.tile_m_y/int(self.grid_params['size'])))

            except ZeroDivisionError:
                pass

            # Handel's exit
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Draws, resets the loop and keeps the framerate capped.
            self.win.blit(grid_surf, (0, 0))#(self.center.x - grid_surf.get_width()/2, self.center.y - grid_surf.get_height()/2))
            pygame.display.update()
            self.clock.tick(self.fps)


# calls main script.
if __name__ == '__main__':
    Main().update()
