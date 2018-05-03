import logging
import pygame
import sys
2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Konstanter
FPS = 60
SCREEN_SIZE = (800, 600)
CAPTION = "Pygame Example"

COLOR = {'ship': pygame.Color('#FF0000'),
         'ship_fill': pygame.Color('#660000'),
         'bg': pygame.Color('#00444c'),
         'thruster': pygame.Color('#7799FF'),
         'fuel_bar': pygame.Color('#440063'),
         'transparent': pygame.Color('#ffffff'),
         'green': pygame.Color('#00ef03')
}

FONT = {'big': None,
        'medium': None,
}

# Game states
STATE_PREGAME = 1
STATE_RUNNING = 2
STATE_GAMEOVER = 3

class Controller():
    """Game controller."""

    def __init__(self):
        """Initialize game controller."""
        self.fps = FPS
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.FONT = {}
        self.FONT['big'] = pygame.font.Font('fonts/Roboto/Roboto-Black.ttf', 30)
        self.FONT['button'] = pygame.font.Font('fonts/Roboto/Roboto-Black.ttf', 30)


        self.player = Player(self.screen)

        # Initialize game state
        self.game_state = STATE_PREGAME

        # Render texts
        self.start_game_text = self.FONT['big'].render('Start game', 13, (100, 100, 100))
        self.gameover_text = self.FONT['big'].render('Game over', 13, (100, 100, 100))
        self.textx = SCREEN_SIZE[0] / 2 - self.start_game_text.get_width()
        self.texty = SCREEN_SIZE[1] / 2 - self.start_game_text.get_height()
        self.textx_quit = SCREEN_SIZE[0] / 2 - self.start_game_text.get_width()
        self.texty_quit = SCREEN_SIZE[1] / 2 - self.start_game_text.get_height()

        self.button_start =  Button(self, 'Start game', SCREEN_SIZE[0] / 4, SCREEN_SIZE[1] - 150, color=(255, 255, 0))
        self.button_restart =  Button(self, 'Restart', SCREEN_SIZE[0] / 4, SCREEN_SIZE[1] - 150, color=(255, 0, 0))


    def run(self):
        """Main game loop."""
        while True:
            # Hantera event för alla states
            # ------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ALT + F4 or icon in upper right corner.
                    self.quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Escape key pressed.
                    self.quit()


                # Hantera _event_ i STATE_PREGAME
                # --------------------------------------------------------------
                if self.game_state == STATE_PREGAME:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = STATE_RUNNING

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.button_start.is_clicked(event):
                            self.player.reset()
                            self.game_state = STATE_RUNNING

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.button_start.is_clicked(event):
                            self.quit()



                # Hantera _event_ i STATE_RUNNING
                # --------------------------------------------------------------
                if self.game_state == STATE_RUNNING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        self.player.engine_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_w:
                        self.player.engine_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                        self.player.right_thruster_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_a:
                        self.player.right_thruster_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                        self.player.left_thruster_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_d:
                        self.player.left_thruster_off()


                # Hantera _event_ i STATE_GAMEOVER
                # --------------------------------------------------------------
                if self.game_state == STATE_GAMEOVER:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.button_restart.is_clicked(event):
                            self.player.reset()
                            self.game_state = STATE_RUNNING


            # Hantera speltillstånd
            # ------------------------------------------------------------------
            if self.game_state == STATE_PREGAME:
                # self.screen.blit
                # Uppritning av start game text
                self.screen.blit(self.start_game_text, (self.textx ,self.texty ))
                self.button_start.draw()


            if self.game_state == STATE_RUNNING:
                self.player.tick()
                # utanför uppe och nere
                if self.player.y > SCREEN_SIZE[1] - 10 or self.player.y < 10:
                    self.game_state = STATE_GAMEOVER
                    # utanför höger och vänster
                if self.player.x > SCREEN_SIZE[0] - 10 or self.player.x < 10:
                    self.game_state = STATE_GAMEOVER
                pygame.draw.lines(self.screen, COLOR['fuel_bar'], 0, ((0,100),(10,10)))
                self.screen.fill(COLOR['bg'])
                self.player.draw()


            if self.game_state == STATE_GAMEOVER:
                #self.quit()  # Gör något bättre.
                self.screen.blit(self.gameover_text, (self.textx ,self.texty ))
                self.button_restart.draw()

            pygame.display.flip()

            self.clock.tick(self.fps)

    def quit(self):
        pygame.quit()
        quit()




class Player():
    def __init__(self, screen):
        self.screen = screen
        self.reset()

    def reset(self):
        self.x = SCREEN_SIZE[0] / 2
        self.y = SCREEN_SIZE[1] / 2
        self.engine = False
        self.left_thruster = False
        self.right_thruster = False
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 20
        self.fuel = 400

    def draw(self):
        surface = pygame.Surface((20, 20), flags=pygame.SRCALPHA)
#        surface.fill(COLOR['transparent'])
#        pygame.draw.line(surface, COLOR['ship'], (10, 0), (15, 20))
#        pygame.draw.line(surface, COLOR['ship'], (10, 0), (5, 20))
        pygame.draw.polygon(surface, COLOR['ship_fill'], ((10, 0), (15, 15), (5, 15)), 0)
        pygame.draw.polygon(surface, COLOR['ship'], ((10, 0), (15, 15), (5, 15)), 1)
        if self.engine:
            pygame.draw.polygon(surface, COLOR['thruster'], ((13, 16), (10, 19), (7, 16)), 0)

        if self.left_thruster:
            pygame.draw.polygon(surface, COLOR['thruster'], ((6, 12), (5, 14), (2, 13), (6, 12), 0))

        if self.right_thruster:
            pygame.draw.polygon(surface, COLOR['thruster'], ((14, 12), (15, 14), (18, 13), (14, 12), 0))

        pygame.draw.lines(self.screen, COLOR['fuel_bar'], 0, [(5,30), (self.fuel,30)], 20)

        self.screen.blit(surface, (self.x - 10, self.y - 10))

    def tick(self):
        # -- Y-axis control
        if self.engine:
            self.y_speed -= 0.01
        else:
            self.y_speed += 0.01

        self.y = self.y + self.y_speed + self.gravity

        # -- X-axis control
        # vänstra motorn
        self.x_speed = self.x_speed * 0.99

        if self.left_thruster:
            self.x_speed += 0.01
        # bränsle för vänstra motorn
        if self.left_thruster == True:
            self.fuel -= 0.51
        if self.fuel < 0:
            self.left_thruster = False
        # högra motorn
        if self.right_thruster:
            self.x_speed -= 0.01
            # bränsle för högra motorn
        if self.right_thruster == True:
            self.fuel -= 0.51
        if self.fuel < 0:
            self.right_thruster = False


        # huvud motorn
        self.x = self.x + self.x_speed
        # bränsle för huvud motorn
        if self.engine == True:
            self.fuel -= 0.51
        if self.fuel < 0:
            self.engine = False

    def engine_on(self):
        self.engine = True

    def engine_off(self):
        self.engine = False

    def left_thruster_on(self):
        self.left_thruster = True

    def left_thruster_off(self):
        self.left_thruster = False

    def right_thruster_on(self):
        self.right_thruster = True

    def right_thruster_off(self):
        self.right_thruster = False


class Button():
    def __init__(self, controller, text, x, y, color=None):
        self.controller = controller
        self.screen = controller.screen
        self.x = x
        self.y = y
        self.border = 5

        text = controller.FONT['button'].render(text, True, (100, 100, 100))
        width, height = text.get_width(), text.get_height()
        color = color if color else (0, 255, 0)
        self.surface = pygame.Surface((width + 2 * self.border, height + 2 * self.border))
        self.surface.fill(color)
        self.surface.blit(text, (self.border, self.border))

    def draw(self):
        width, height = self.surface.get_width(), self.surface.get_height()
        pos = (self.x - width / 2, self.y - height / 2)

        self.screen.blit(self.surface, pos)

    def tick(self):
        pass  # Antagligen inte så användbart

    def is_clicked(self, event):
        click_x, click_y = event.pos
        width, height = self.surface.get_width(), self.surface.get_height()

        if click_x > self.x - width / 2 and click_x < self.x + width / 2 and click_y > self.y - height / 2 and click_y < self.y + height / 2:
            return True

        return False


if __name__ == "__main__":
    logger.info('Starting...')
    c = Controller()
    c.run()
