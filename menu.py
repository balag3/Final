import pygame
import sys
from main_joy import *

pygame.init()


class GameMenu():
    def __init__(self, screen, items, bg_color=(0, 0, 0), font=None, font_size=50,
                 font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy)])

    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                    done = True
                    sys.exit(0)

            try:
               pygame.joystick.init()
               joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
               joysticks[0].init()
               joysticks[1].init()
               player1_joystick = joysticks[0]
               player2_joystick = joysticks[1]
            except IndexError:
               player1_joystick = None
               player2_joystick = None


            pressed = pygame.key.get_pressed()
            # Up
            if pressed[pygame.K_1]:
                main()

            # Down
            if pressed[pygame.K_2]:
                running = False
                sys.exit(0)


            if event.type == pygame.JOYBUTTONDOWN:
                if player1_joystick.get_button(0):
                    running = False
                    sys.exit(0)
                if player2_joystick.get_button(0):
                    running = False
                    sys.exit(0)

            if event.type == pygame.JOYBUTTONUP:
                if player1_joystick.get_button(0):
                    main()
                if player2_joystick.get_button(0):
                    main()


            # Redraw the background
            self.screen.fill(self.bg_color)

            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()


if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((1280, 800), 0, 32)

    menu_items = ('Start', 'Quit')

    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()
