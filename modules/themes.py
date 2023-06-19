import pygame
import time
from utils.tools import resource_path
from utils.constants import *

class ColorTheme:

    def __init__(self):
        self.color = None
        self.theme_logo = pygame.image.load(resource_path('img/theme.png')).convert_alpha()
        self.theme_button = None
        self.bar_position = False
        self.theme_clicked = False
        self.theme_font = pygame.font.Font(None, 32)
        self.themelist = []
        self.theme_colors = {'dark_blue': ("#0D151B", "#4CC2F0"), 'dark_red': ("#1B1B1B", "#FF2470"),
                             'dark_green': ("#151014", "#379534"), 'dark_yellow': ("#181818", "#9C8F5D"),
                             'light_blue': ("#FFFFFF", "#66A0BF"), 'light_red': ("#FFFFFF", "#C16469"),
                             'grey_green': ("#383B35", "#AEC99E")
                             }
        return

    def themebutton(self):
        """This function is for drawing the """
        self.theme_button = pygame.draw.circle(surface, safety_secondary_color, (WIDTH-25, 25), 20)
        surlogo = surface.blit(self.theme_logo, self.theme_logo.get_rect(center=self.theme_button.center))
        pygame.display.update([surlogo, self.theme_button])
        return

    def themeselector(self):
        """Function draws possible color combos and displays them in two columns"""
        text_surface = self.theme_font.render("Pick a Theme!", True, (255-safety_base_color.r, 255-safety_base_color.g, 255-safety_base_color.b))
        theme_text = pygame.draw.rect(surface, safety_base_color, (WIDTH / 2 - 100, 50, 200, 50))
        surface.blit(text_surface, (theme_text.x + (theme_text.width / 4 - 25), theme_text.y + (theme_text.height / 4)))
        ck = [*self.theme_colors]
        ck_co = 0
        for y in range(1, 6):
            for x in range(1, 3):
                for i in range(25):
                    if ck_co > len(ck) - 1:
                        return
                    time.sleep(0.001)
                    if i == 24:
                        self.themelist += [pygame.draw.circle(surface, self.theme_colors[ck[ck_co]][0], (WIDTH * (x / 3), HEIGHT * (y / 5)), 0 + i)]
                    else:
                        pygame.draw.circle(surface, self.theme_colors[ck[ck_co]][0], (WIDTH * (x / 3), HEIGHT * (y / 5)), 0 + i)
                    if 25 >= i >= 10:
                        pygame.draw.circle(surface, self.theme_colors[ck[ck_co]][1], (WIDTH * (x / 3), HEIGHT * (y / 5)), -10 + i)
                    pygame.display.flip()
                ck_co += 1

    def expandocircle(self, slider_pos=None):
        """A function to animate the expanding theme selector

        :param slider_pos: To either close or open the theme selector
        :return:
        """
        if slider_pos is None:
            return
        if slider_pos:  # open theme selector
            for i in range(HEIGHT):
                if HEIGHT-i == 50:
                    continue
                circle_pos = (WIDTH-25, 25)
                pygame.draw.circle(surface, safety_secondary_color, circle_pos, 20+i+3)
                pygame.draw.circle(surface, safety_base_color, circle_pos, 20+i+1)
                self.themebutton()
                pygame.display.update()
            self.themeselector()

        elif not slider_pos:  # close theme selector
            for i in range(HEIGHT):
                if HEIGHT-i == 20:
                    return False

                if menu.startgame:
                    board.drawlayout()
                else:
                    main_menu()
                circle_pos = (WIDTH - 25, 25)
                pygame.draw.circle(surface, safety_secondary_color, circle_pos, 800-i-1)
                pygame.draw.circle(surface, safety_base_color, circle_pos, 800-i-3)
                self.themebutton()
                pygame.display.update()
        return

    def themeevent(self, event) -> bool:
        """Function to switch between the different themes on mouse press

        :return: Boolean if theme selector is open
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.theme_button.collidepoint(event.pos) and not self.bar_position:
                self.expandocircle(True)
                self.bar_position = True
            elif self.theme_button.collidepoint(event.pos) and self.bar_position:
                self.expandocircle(False)
                self.bar_position = False

            if self.bar_position:
                for i, bg in enumerate(self.themelist):
                    if bg.collidepoint(event.pos) and self.bar_position:
                        global safety_base_color, safety_secondary_color, safety_base_inverse, safety_secondary_inverse

                        safety_base_color = pygame.Color(list(self.theme_colors.values())[i][0])
                        safety_secondary_color = pygame.Color(list(self.theme_colors.values())[i][1])
                        safety_base_inverse = pygame.Color(255-safety_base_color.r, 255-safety_base_color.b, 255-safety_base_color.g)
                        safety_secondary_inverse = pygame.Color(255-safety_secondary_color.r, 255-safety_secondary_color.b, 255-safety_secondary_color.g)

                        self.expandocircle(True)
                        break

        return self.bar_position
