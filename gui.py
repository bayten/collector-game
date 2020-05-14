import pygame
import images
import utils as ut

GAME_FONT = 'FortunataCYR.ttf'


class GuiObject:
    def __init__(self, pos, size, trigger_name=None):
        self.pos = pos
        self.size = size
        self.focus = False
        self.is_pressed = False
        self.trigger_name = trigger_name

    def includes(self, mouse_pos):
        if self.pos[0] <= mouse_pos[0] <= self.pos[0]+self.size[0] and\
           self.pos[1] <= mouse_pos[1] <= self.pos[1]+self.size[1]:
            return True
        return False

    def init_pdown(self, mouse_pos, triggers):
        pass

    def next_pdown(self, mouse_pos, triggers):
        pass

    def init_pup(self, mouse_pos, triggers):
        pass

    def can_focus(self, mouse_pos):
        if self.includes(mouse_pos):
            return True
        return False

    def draw(self, surface, triggers, mouse_pos):
        pass


class TextBox(GuiObject):
    def __init__(self, pos, size, text, font_path, color=(0, 0, 0),
                 color_s=(0, 0, 0), color_p=(0, 0, 0)):
        super().__init__(pos, size)
        self.text = text
        self.color = color
        self.color_p = color_p
        self.color_s = color_s

        possible_text_size = 10
        while True:
            test_font = pygame.font.Font(font_path, possible_text_size)
            test_font_size = test_font.size(self.text)
            if test_font_size[0] > size[0] or test_font_size[1] > size[1]:
                break
            possible_text_size += 1
        self.font = pygame.font.Font(font_path, possible_text_size-1)

    def can_focus(self, mouse_pos):
        return False

    def draw(self, surface, mouse_pos, triggers):
        if self.is_pressed:
            text_surface = self.font.render(self.text, True, self.color_p)
        if self.includes(mouse_pos):
            text_surface = self.font.render(self.text, True, self.color_s)
        else:
            text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, self.pos)


class FixedImage(GuiObject):
    def __init__(self, pos, size, image=None):
        super().__init__(pos, size)
        if image:
            self.image = pygame.transform.scale(image, self.size)
        else:
            self.image = image

    def can_focus(self, mouse_pos):
        return False

    def draw(self, surface, mouse_pos, triggers):
        surface.blit(self.image, self.pos)


class Button(GuiObject):
    def __init__(self, pos, size, tname, image, image_pressed=None, text=None):
        super().__init__(pos, size, tname)

        self.image = pygame.transform.scale(image, size)
        if image_pressed:
            self.image_pressed = pygame.transform.scale(image_pressed, size)

        else:
            self.image_pressed = self.image

        if text:
            text_pos = pos[0] + 0.08*size[0], pos[1] + 0.25*size[1]
            text_size = 0.85*size[0], 0.8*size[1]
            self.text = TextBox(text_pos, text_size, *text)
        else:
            self.text = None

    def init_pdown(self, mouse_pos, triggers):
        self.is_pressed = True
        if self.text:
            self.text.is_pressed = True

    def next_pdown(self, mouse_pos, triggers):
        pass

    def init_pup(self, mouse_pos, triggers):
        self.is_pressed = False
        if self.text:
            self.text.is_pressed = False
        for trigger_idx, trigger in enumerate(triggers):
            tname, tval, tmax_val = trigger
            if tname == self.trigger_name:
                triggers[trigger_idx] = tname, (tval+1) % tmax_val, tmax_val
                break

    def draw(self, surface, mouse_pos, triggers):
        if self.is_pressed:
            surface.blit(self.image_pressed, self.pos)
        else:
            surface.blit(self.image, self.pos)
        if self.text:
            self.text.draw(surface, mouse_pos, triggers)


class MenuMode:
    '''Basic ьутг mode'''
    def __init__(self, menu_img, menu_pos=(0, 0), gui=None, triggers=None):
        '''Set game mode up

        - Initialize field'''

        self.menu_img = menu_img
        self.back_img = None
        self.menu_pos = menu_pos  # left upper corner
        self.cursor_img = images.CURSOR_IMG
        self.gui = gui
        self.focused = None
        self.pressed_down = False
        self.triggers = triggers

    def update_focus(self, mouse_pos):
        if self.focused:
            if self.gui[self.focused].includes(mouse_pos):
                return
            self.gui[self.focused].focus = False
            self.focused = None

        focus_candidates = []
        for idx, gui in enumerate(self.gui):
            if gui.can_focus(mouse_pos):
                focus_candidates.append(idx)

        # any sort of solving focus conflicts.. for example, first one
        if focus_candidates:
            self.focused = focus_candidates[0]
            self.gui[self.focused].focus = True

    def Events(self, events, screen):
        '''Event parser'''
        for event in events:
            if event.type is pygame.QUIT:
                return False

            elif event.type is pygame.MOUSEBUTTONDOWN:
                self.update_focus(event.pos)
                if self.focused:
                    self.pressed_down = True
                    self.gui[self.focused].init_pdown(event.pos, self.triggers)
            elif event.type is pygame.MOUSEMOTION and self.pressed_down:
                if self.focused:
                    self.gui[self.focused].next_pdown(event.pos, self.triggers)
            elif event.type is pygame.MOUSEBUTTONUP:
                if self.focused:
                    self.gui[self.focused].init_pup(event.pos, self.triggers)
                    self.pressed_down = False
        return True

    def Draw(self, screen):
        '''Draw game field'''
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(self.back_img, (0, 0))
        screen.blit(self.menu_img, self.menu_pos)
        for gui in self.gui:
            gui.draw(screen, mouse_pos, self.triggers)

        screen.blit(self.cursor_img, mouse_pos)

    def Leave(self):
        '''What to do when leaving this mode'''
        pygame.mouse.set_visible(True)
        return self.triggers

    def Init(self, screen):
        '''What to do when entering this mode'''
        pygame.mouse.set_visible(False)
        self.back_img = screen.copy()


class CloseDialog(MenuMode):
    def __init__(self):
        triggers = [('close', 0, 2), ('accept', 0, 2)]

        dialog_size = (400, 300)
        pos_x = ut.BSIZE[0]*ut.TILE/2-dialog_size[0]/2
        pos_y = ut.BSIZE[1]*ut.TILE/2-dialog_size[1]/2

        cls_pos = pos_x+50, pos_y+150
        acc_pos = pos_x+250, pos_y+150
        text_pos = pos_x+50, pos_y+20
        b_size = (100, 100)
        cls = Button(cls_pos, b_size, 'close', images.BUTT_CLS_IMG)
        acc = Button(acc_pos, b_size, 'accept', images.BUTT_ACC_IMG)

        text = TextBox(text_pos, (300, 200), 'Что, уже?', GAME_FONT)

        splash = pygame.transform.scale(images.SPLASH_IMG, dialog_size)
        super().__init__(splash, (pos_x, pos_y), [text, cls, acc], triggers)

    def MainLoop(self, screen):
        self.Init(screen)
        while True:
            events = pygame.event.get()
            self.Events(events, screen)
            self.Draw(screen)
            pygame.display.flip()

            if self.triggers[0][1] == 1:
                self.Leave()
                return False
            elif self.triggers[1][1] == 1:
                self.Leave()
                return True

    def Events(self, events, screen):
        '''Event parser'''
        for event in events:
            if event.type is pygame.MOUSEBUTTONDOWN:
                self.update_focus(event.pos)
                if self.focused:
                    self.pressed_down = True
                    self.gui[self.focused].init_pdown(event.pos, self.triggers)
            elif event.type is pygame.MOUSEMOTION and self.pressed_down:
                if self.focused:
                    self.gui[self.focused].next_pdown(event.pos, self.triggers)
            elif event.type is pygame.MOUSEBUTTONUP:
                if self.focused:
                    self.gui[self.focused].init_pup(event.pos, self.triggers)
                    self.pressed_down = False
        return True


class SplashScreen(MenuMode):
    def __init__(self, title_text, text1, text2):
        triggers = [('restart', 0, 2), ('menu', 0, 2)]

        dialog_size = (500, 500)
        pos_x = ut.BSIZE[0]*ut.TILE/2-dialog_size[0]/2
        pos_y = ut.BSIZE[1]*ut.TILE/2-dialog_size[1]/2

        menu_pos = pos_x+25, pos_y+400
        res_pos = pos_x+275, pos_y+400
        title_pos = pos_x, pos_y
        text1_pos = pos_x+50, pos_y+150
        text2_pos = pos_x+50, pos_y+300

        b_size = (200, 100)

        menu_text = ('МЕНЮ', GAME_FONT)
        restart_text = ('ЗАНОВО', GAME_FONT)
        menu = Button(menu_pos, b_size, 'menu', images.BUTT_TMP_IMG,
                      images.BUTT_TMP_PRESSED_IMG, menu_text)
        restart = Button(res_pos, b_size, 'restart', images.BUTT_TMP_IMG,
                         images.BUTT_TMP_PRESSED_IMG, restart_text)

        title_text_box = TextBox(title_pos, (500, 200), title_text, GAME_FONT)
        text1_box = TextBox(text1_pos, (400, 100), text1, GAME_FONT)
        text2_box = TextBox(text2_pos, (400, 100), text2, GAME_FONT)

        splash = pygame.transform.scale(images.SPLASH_IMG, dialog_size)
        my_gui = (title_text_box, text1_box, text2_box, menu, restart)
        super().__init__(splash, (pos_x, pos_y), my_gui, triggers)

    def MainLoop(self, screen):
        self.Init(screen)
        while True:
            events = pygame.event.get()
            game_trigger = self.Events(events, screen)

            if not game_trigger:
                self.Leave()
                return False

            self.Draw(screen)
            pygame.display.flip()

            if self.triggers[0][1] == 1:
                self.Leave()
                return True
            elif self.triggers[1][1] == 1:
                self.Leave()
                return False

    def Events(self, events, screen):
        '''Event parser'''
        for event in events:
            if event.type is pygame.QUIT:
                dialog = CloseDialog()
                if dialog.MainLoop(screen):
                    return False
            if event.type is pygame.MOUSEBUTTONDOWN:
                self.update_focus(event.pos)
                if self.focused:
                    self.pressed_down = True
                    self.gui[self.focused].init_pdown(event.pos, self.triggers)
            elif event.type is pygame.MOUSEMOTION and self.pressed_down:
                if self.focused:
                    self.gui[self.focused].next_pdown(event.pos, self.triggers)
            elif event.type is pygame.MOUSEBUTTONUP:
                if self.focused:
                    self.gui[self.focused].init_pup(event.pos, self.triggers)
                    self.pressed_down = False
        return True
