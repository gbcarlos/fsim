import pygame

BEIGE = (249,228,183)
BLACK = (0,0,0)

class DropDown():

    def __init__(self, x, y, w, h, option_list, selected=0, label=""):
        self.color = pygame.Color('chartreuse4')
        self.highlight_color = pygame.Color('lightskyblue3')
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont('Calibri', 20)
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False # Active when mouse over menu rect
        self.active_option = -1
        self.base_font = pygame.font.SysFont('Calibri', 20)
        self.label = label

    def draw(self, surf):
        # Surface for dropdown with all options (3 options = Selection rect + 3x Option Rect size)
        dd_unfolded_rect = [self.rect.x, self.rect.y, self.rect.w, (len(self.option_list) + 1)*self.rect.h]
        pygame.draw.rect(surf, BEIGE, dd_unfolded_rect)
        pygame.draw.rect(surf, BEIGE, dd_unfolded_rect, 2)

        # Dropdown Label
        label_surface = self.base_font.render(self.label, True, BLACK)
        label_rect = label_surface.get_rect()
        label_rect.center = (self.rect.x - label_rect.w/2 - 5, self.rect.y + self.rect.h/2)
        surf.blit(label_surface, label_rect)

        # Dropdown
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, BLACK, self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, BLACK)
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, BLACK)
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
            self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, BLACK, outer_rect, 2)

    def update(self, event):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        # If mouse is left clicked (event.button == 1)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.selected = self.active_option
                self.draw_menu = False
                return self.active_option
        return -1