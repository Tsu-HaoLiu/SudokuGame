import pygame

from utils.tools import resource_path
from utils.constants import *

class MainMenu:
    def __init__(self):
        self.newgame_button = []
        self.startgame = False
        self.left_arr = None
        self.right_arr = None
        self.render_diff = None
        self.base_font = pygame.font.Font(None, 32)
        self.diff_txt = pygame.font.Font(None, 24)
        self.logo = pygame.image.load(resource_path('img/main_logo.png')).convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (100, 100))
        self.logo = pygame.transform.rotate(self.logo, 45)

        self.difficulty = ['Beginner', 'Easy', 'Medium', 'Hard', 'Extreme']
        self.diff_iter = 0

    def diff(self):
        return self.difficulty[self.diff_iter]

    def fade(self, w, h, slide, side):
        """Function to animate the difficulty selector horizontal scroll when arrow is pressed"""
        fade = pygame.Surface((w, h))
        fade.fill(safety_base_color)

        if side == "right":
            if slide < 0:
                fade.set_alpha(abs(slide)*4)
            elif slide >= 0:
                fade.set_alpha(slide)
        elif side == "left":
            if slide < 0:
                fade.set_alpha(255-slide*2)
            elif slide >= 0:
                fade.set_alpha(slide*4)

        surface.blit(fade, (WIDTH/3+41+slide, HEIGHT/2+30, 75, 25))
        pygame.display.flip()
        pygame.time.delay(5)

    def draw_static_menu(self):
        """Function to load the main menu"""
        # print(WIDTH, HEIGHT)
        # print(surface)

        surface.fill(safety_base_color)

        cir = pygame.draw.circle(surface, safety_secondary_color, (WIDTH/2, HEIGHT/3), 75)
        surface.blit(self.logo, self.logo.get_rect(center=cir.center))

        text_surface = self.base_font.render("New Game", True, safety_base_color)

        self.left_arr = pygame.draw.lines(surface, safety_base_inverse, False, [(WIDTH/4, HEIGHT/2+50), (WIDTH/4-8, HEIGHT/2+50-8), (WIDTH/4, HEIGHT/2+50-16)], 5)
        self.right_arr = pygame.draw.lines(surface, safety_base_inverse, False, [(WIDTH-(WIDTH/4), HEIGHT/2+50), (WIDTH-(WIDTH/4)+8, (HEIGHT/2)+50-8), (WIDTH-(WIDTH/4), (HEIGHT/2)+50-16)], 5)

        self.newgame_button = [pygame.draw.circle(surface, safety_secondary_color, (WIDTH/4, HEIGHT/2+100), 25),
                               pygame.draw.circle(surface, safety_secondary_color, (WIDTH-(WIDTH/4), HEIGHT / 2 + 100), 25),
                               pygame.draw.rect(surface, safety_secondary_color, (WIDTH/4, HEIGHT/2+100-25, 245, 50))]

        surface.blit(text_surface, (
            self.newgame_button[-1].x + (self.newgame_button[-1].width/4+5),
            self.newgame_button[-1].y + (self.newgame_button[-1].height/4+2)
        ))
        return

    def draw_dynamic_menu(self, i=0):
        """Draw scrolling difficulty animation box"""
        pygame.draw.rect(surface, safety_base_color, (WIDTH/3+41+i, HEIGHT/2+30, 75, 25))
        self.render_diff = self.diff_txt.render(self.difficulty[self.diff_iter], True, safety_base_inverse)
        txwid = self.render_diff.get_width()
        surface.blit(self.render_diff, ((WIDTH/2)-(txwid/2)+i, HEIGHT*2/4+36))
        return

    def draw_full_menu(self):
        self.draw_static_menu()
        self.draw_dynamic_menu()

    def mouse_press(self, event):
        """Function to detect mouse press for main menu difficulty scroll animation"""
        event.pos = (0, 0) if not hasattr(event, 'pos') else event.pos
        event.key = 0 if not hasattr(event, 'key') else event.key

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            if self.left_arr.collidepoint(event.pos) or event.key == pygame.K_LEFT:
                # move difficulty selector to the left
                for slide in range(80):
                    self.draw_dynamic_menu(slide)
                    if slide >= 50:
                        self.fade(75, 25, slide, "left")
                if self.diff_iter != 0:
                    self.diff_iter -= 1
                for slide in reversed(range(80)):
                    self.draw_dynamic_menu(-slide)
                    if slide <= 20:
                        self.fade(75, 25, -slide, "left")

            elif self.right_arr.collidepoint(event.pos) or event.key == pygame.K_RIGHT:
                # move difficulty selector to the right
                for slide in range(80):
                    self.draw_dynamic_menu(-slide)
                    if slide >= 50:
                        self.fade(75, 25, -slide, "right")
                if self.diff_iter != len(self.difficulty) - 1:
                    self.diff_iter += 1
                for slide in reversed(range(80)):
                    self.draw_dynamic_menu(slide)
                    if slide <= 20:
                        self.fade(75, 25, slide, "right")
            pygame.display.flip()

    def startplaying(self, event):
        """Function to start the game if new game button is pressed"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            newgame_button = [x for x in self.newgame_button if x.collidepoint(event.pos)]

            if not self.startgame and newgame_button:
                self.startgame = True
                return self.startgame
        return False