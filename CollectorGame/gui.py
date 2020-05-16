"""
gui.py -- GUI submodule
=======================
This is module, which contains GUI Classes.
"""

import pygame  # type: ignore
from typing import List, Tuple, Optional, Callable
import CollectorGame.images as images
import CollectorGame.utils as ut


class GuiObject:
    """General entity of basic GUI object"""
    def __init__(self, pos: ut.Coord, size: ut.Size,
                 trigger_name: Optional[str] = None) -> None:
        """Initialise GUI object"""
        x = max(0, min(pos[0], ut.BSIZE[0]*ut.TILE-1))
        y = max(0, min(pos[1], ut.BSIZE[1]*ut.TILE-1))
        self.pos: ut.Coord = (x, y)

        sx = max(1, min(size[0], ut.BSIZE[0]*ut.TILE-1))
        sy = max(1, min(size[1], ut.BSIZE[1]*ut.TILE-1))
        self.size: ut.Size = (sx, sy)

        self.focus: bool = False
        self.is_pressed: bool = False
        self.trigger_name: Optional[str] = trigger_name

    def includes(self, mouse_pos: ut.Coord) -> bool:
        """Check if given position is included in object's area"""
        if self.pos[0] <= mouse_pos[0] <= self.pos[0]+self.size[0] and\
           self.pos[1] <= mouse_pos[1] <= self.pos[1]+self.size[1]:
            return True
        return False

    def init_pdown(self, mouse_pos: ut.Coord,
                   triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Process initial event of mouse key pressed down"""
        pass

    def next_pdown(self, mouse_pos: ut.Coord,
                   triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Process subsequent event of not-released pressed down mouse key"""
        pass

    def init_pup(self, mouse_pos: ut.Coord,
                 triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Process event of mouse key being released"""
        pass

    def can_focus(self, mouse_pos: ut.Coord) -> bool:
        """Check if this GUI object can get focused with given mouse pos"""
        if self.includes(mouse_pos):
            return True
        return False

    def draw(self, surface: ut.Image,
             mouse_pos: ut.Coord,
             triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Draw GUI object on the given surface"""
        pass


class TextBox(GuiObject):
    """Primitive textbox element"""
    def __init__(self, pos: ut.Coord,
                 size: ut.Size,
                 text: str,
                 font_path: str,
                 color: pygame.Color = (0, 0, 0),
                 color_s: pygame.Color = (0, 0, 0),
                 color_p: pygame.Color = (0, 0, 0)) -> None:
        """Initialise textbox"""
        super().__init__(pos, size)
        if not pygame.font.get_init():
            pygame.font.init()

        self.text: str = text
        self.color: pygame.Color = color
        self.color_p: pygame.Color = color_p
        self.color_s: pygame.Color = color_s

        text_size = 10
        while True:
            test_font = pygame.font.Font(font_path, text_size)
            test_font_size = test_font.size(self.text)
            if test_font_size[0] > size[0] or test_font_size[1] > size[1]:
                break
            text_size += 1
        self.font: pygame.font.Font = pygame.font.Font(font_path, text_size-1)

    def can_focus(self, mouse_pos: ut.Coord) -> bool:
        """Textbox cannot get focused in any case"""
        return False

    def draw(self, surface: ut.Image,
             mouse_pos: ut.Coord,
             triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Draw textbox on the given surface"""
        if self.is_pressed:
            text_surface = self.font.render(self.text, True, self.color_p)
        if self.includes(mouse_pos):
            text_surface = self.font.render(self.text, True, self.color_s)
        else:
            text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, self.pos)


class FixedImage(GuiObject):
    """Primitive image element"""
    def __init__(self, pos: ut.Coord,
                 size: ut.Size,
                 image: Optional[ut.Image] = None) -> None:
        """Initialise FixedImage"""
        super().__init__(pos, size)
        self.image: Optional[ut.Image] = None
        if image:
            self.image = pygame.transform.scale(image, self.size)

    def can_focus(self, mouse_pos: ut.Coord) -> bool:
        """Fixed image cannot get focused in any case"""
        return False

    def draw(self, surface: ut.Image,
             mouse_pos: ut.Coord,
             triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Draw FixedImage on the given surface"""
        surface.blit(self.image, self.pos)


class Button(GuiObject):
    """Multifunctional button (optionally with text caption)"""
    def __init__(self, pos: ut.Coord,
                 size: ut.Size,
                 tname: str,
                 image: ut.Image,
                 image_p: Optional[ut.Image] = None,
                 text: Optional[Tuple[str, str]] = None,
                 bfunc: Callable[[int, int], int] = ut.bfunc_minc) -> None:
        """Initialise Button element"""
        super().__init__(pos, size, tname)

        self.image: ut.Image = pygame.transform.scale(image, self.size)
        self.image_pressed: Optional[ut.Image] = None
        if image_p:
            self.image_pressed = pygame.transform.scale(image_p, self.size)

        self.bfunc = bfunc
        self.text: Optional[TextBox] = None
        if text:
            text_pos_x = int(self.pos[0] + 0.08*self.size[0])
            text_pos_y = int(self.pos[1] + 0.25*self.size[1])
            text_size = int(0.85*self.size[0]), int(0.8*self.size[1])
            self.text = TextBox((text_pos_x, text_pos_y), text_size, *text)

    def init_pdown(self, mouse_pos: ut.Coord,
                   triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Process initial event of mouse key pressed down"""
        if self.includes(mouse_pos):
            self.is_pressed = True
            if self.text:
                self.text.is_pressed = True

    def init_pup(self, mouse_pos: ut.Coord,
                 triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Process event of mouse key being released"""
        self.is_pressed = False
        if self.text:
            self.text.is_pressed = False
        if triggers is not None:
            for t_idx, trigger in enumerate(triggers):
                tname, tval, tmax_val = trigger
                if tname == self.trigger_name:
                    tnew_val = self.bfunc(tval, tmax_val)
                    triggers[t_idx] = tname, tnew_val, tmax_val
                    break

    def draw(self, surface: ut.Image,
             mouse_pos: ut.Coord,
             triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Draw Button element on the given surface"""
        if self.is_pressed:
            if self.image_pressed:
                surface.blit(self.image_pressed, self.pos)
            else:
                surface.blit(self.image, self.pos)
        else:
            surface.blit(self.image, self.pos)
        if self.text:
            self.text.draw(surface, mouse_pos, triggers)


class MenuMode:
    """Basic menu mode"""
    def __init__(self, menu_img: ut.Image,
                 menu_pos: ut.Coord = (0, 0),
                 gui: Optional[List[GuiObject]] = None,
                 triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Set menu mode up"""

        self.menu_img: ut.Image = menu_img
        self.back_img: Optional[ut.Image] = None
        x = max(0, min(menu_pos[0], ut.BSIZE[0] * ut.TILE - 1))
        y = max(0, min(menu_pos[1], ut.BSIZE[1] * ut.TILE - 1))
        self.menu_pos: ut.Coord = (x, y)  # left upper corner
        self.cursor_img: ut.Image = images.CURSOR_IMG
        self.gui: Optional[List[GuiObject]] = gui
        self.focused: Optional[int] = None
        self.pressed_down: bool = False
        self.triggers: Optional[List[ut.Trigger]] = triggers

    def init(self, screen: ut.Image) -> None:
        """What to do when entering this mode"""
        pygame.mouse.set_visible(False)
        self.back_img = screen.copy()

    def update_focus(self, mouse_pos: ut.Coord) -> None:
        """Calculate new focused GUI object, if possible"""
        if self.gui is None:
            return

        if self.focused:
            if self.gui[self.focused].includes(mouse_pos):
                return
            self.gui[self.focused].focus = False
            self.focused = None

        focus_candidates: List[int] = []
        for idx, gui in enumerate(self.gui):
            if gui.can_focus(mouse_pos):
                focus_candidates.append(idx)

        # any sort of solving focus conflicts.. for example, first one
        if focus_candidates:
            self.focused = focus_candidates[0]
            self.gui[self.focused].focus = True

    def events(self, events: List[ut.Event],
               screen: ut.Image) -> bool:
        """Event parser: process all events from previous tick"""
        for event in events:
            if event.type is pygame.QUIT:
                return False

            elif event.type is pygame.MOUSEBUTTONDOWN:
                self.update_focus(event.pos)
                if self.focused and self.gui:
                    self.pressed_down = True
                    self.gui[self.focused].init_pdown(event.pos, self.triggers)
            elif event.type is pygame.MOUSEMOTION and self.pressed_down:
                if self.focused and self.gui:
                    self.gui[self.focused].next_pdown(event.pos, self.triggers)
            elif event.type is pygame.MOUSEBUTTONUP:
                if self.focused and self.gui:
                    self.gui[self.focused].init_pup(event.pos, self.triggers)
                    self.pressed_down = False
        return True

    def draw(self, screen: ut.Image) -> None:
        """Draw all GUI objects"""
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(self.back_img, (0, 0))
        screen.blit(self.menu_img, self.menu_pos)
        if self.gui:
            for gui in self.gui:
                gui.draw(screen, mouse_pos, self.triggers)

        screen.blit(self.cursor_img, mouse_pos)

    def leave(self) -> Optional[List[ut.Trigger]]:
        """What to do when leaving this mode"""
        pygame.mouse.set_visible(True)
        return self.triggers


class CloseDialog(MenuMode):
    """Primitive close dialog to process QUIT event"""
    def __init__(self) -> None:
        """Initialise CloseDialog"""
        dialog_size = (400, 300)
        pos_x = int(ut.BSIZE[0]*ut.TILE/2-dialog_size[0]/2)
        pos_y = int(ut.BSIZE[1]*ut.TILE/2-dialog_size[1]/2)
        splash = pygame.transform.scale(images.SPLASH_IMG, dialog_size)

        super().__init__(splash, (pos_x, pos_y))

        cls_pos = pos_x+50, pos_y+150
        acc_pos = pos_x+250, pos_y+150
        text_pos = pos_x+50, pos_y+20
        b_size = (100, 100)
        cls = Button(cls_pos, b_size, 'close', images.BUTT_CLS_IMG)
        acc = Button(acc_pos, b_size, 'accept', images.BUTT_ACC_IMG)

        text = TextBox(text_pos, (300, 200), 'Что, уже?', ut.GAME_FONT)
        triggers = [('close', 0, 2), ('accept', 0, 2)]

        self.gui: List[GuiObject] = [text, cls, acc]
        self.triggers: List[ut.Trigger] = triggers

    def main_loop(self, screen: ut.Image) -> bool:
        """Subsequently process all procedures for CloseDialog"""
        self.init(screen)
        while True:
            events = pygame.event.get()
            self.events(events, screen)
            self.draw(screen)
            pygame.display.flip()

            if self.triggers[0][1] == 1:
                self.leave()
                return False
            elif self.triggers[1][1] == 1:
                self.leave()
                return True

    def events(self, events: List[ut.Event],
               screen: ut.Image) -> bool:
        """Event parser: process all events from previous tick"""
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
    """Primitive splash screen

    Show results of your game + give options to restart or quit.
    """

    def __init__(self, title_text: str,
                 text1: str,
                 text2: str) -> None:
        """Initialise SplashScreen"""
        dialog_size = (500, 500)
        pos_x = int(ut.BSIZE[0]*ut.TILE/2-dialog_size[0]/2)
        pos_y = int(ut.BSIZE[1]*ut.TILE/2-dialog_size[1]/2)
        splash = pygame.transform.scale(images.SPLASH_IMG, dialog_size)

        super().__init__(splash, (pos_x, pos_y))

        menu_pos = pos_x, pos_y+400
        help_pos = pos_x+175, pos_y+400
        res_pos = pos_x+350, pos_y+400
        title_pos = pos_x, pos_y
        text1_pos = pos_x+50, pos_y+150
        text2_pos = pos_x+50, pos_y+300

        b_size = (150, 100)

        menu_text = ('МЕНЮ', ut.GAME_FONT)
        help_text = ('ПОМОЩЬ', ut.GAME_FONT)
        restart_text = ('ЗАНОВО', ut.GAME_FONT)

        menu = Button(menu_pos, b_size, 'menu', images.BUTT_TMP_IMG,
                      images.BUTT_TMP_PRESSED_IMG, menu_text)
        help = Button(help_pos, b_size, 'help', images.BUTT_TMP_IMG,
                      images.BUTT_TMP_PRESSED_IMG, help_text)

        restart = Button(res_pos, b_size, 'restart', images.BUTT_TMP_IMG,
                         images.BUTT_TMP_PRESSED_IMG, restart_text)

        title_box = TextBox(title_pos, (500, 200), title_text, ut.GAME_FONT)
        text1_box = TextBox(text1_pos, (400, 100), text1, ut.GAME_FONT)
        text2_box = TextBox(text2_pos, (400, 100), text2, ut.GAME_FONT)

        my_gui = [title_box, text1_box, text2_box, menu, help, restart]
        self.gui: List[GuiObject] = my_gui

        triggers = [('restart', 0, 2), ('menu', 0, 2), ('help', 0, 2)]
        self.triggers: List[ut.Trigger] = triggers

    def main_loop(self, screen: ut.Image) -> bool:
        """Subsequently process all procedures for SplashScreen"""
        self.init(screen)
        while True:
            events = pygame.event.get()
            game_trigger = self.events(events, screen)

            if not game_trigger:
                self.leave()
                return False

            self.draw(screen)
            pygame.display.flip()

            if self.triggers[0][1] == 1:
                self.leave()
                return True
            elif self.triggers[1][1] == 1:
                self.leave()
                return False
            elif self.triggers[2][1] == 1:
                help_dialog = HelpScreen()
                if help_dialog.main_loop(screen) is False:
                    self.leave()
                    return False
                self.triggers[2] = self.triggers[2][0], 0, self.triggers[2][2]

    def events(self, events: ut.Event,
               screen: ut.Image) -> bool:
        """Event parser: process all events from previous tick"""
        for event in events:
            if event.type is pygame.QUIT:
                dialog = CloseDialog()
                if dialog.main_loop(screen):
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


class HelpScreen(MenuMode):
    """Primitive help screen

    Show results of your game + give options to restart or quit.
    """

    def __init__(self) -> None:
        """Initialise HelpScreen"""
        dialog_size = (ut.BSIZE[0] * ut.TILE, ut.BSIZE[1] * ut.TILE)
        pos_x = int(ut.BSIZE[0] * ut.TILE / 2 - dialog_size[0] / 2)
        pos_y = int(ut.BSIZE[1] * ut.TILE / 2 - dialog_size[1] / 2)

        menu_img = pygame.transform.scale(images.MENU_IMG, dialog_size)
        super().__init__(menu_img, (pos_x, pos_y))

        title_pos = int(0.1*dialog_size[0]), int(0.1*dialog_size[1])
        title_size = int(0.8*dialog_size[0]), int(0.5*dialog_size[1])
        title_box = TextBox(title_pos, title_size, "ПОМОЩЬ", ut.GAME_FONT)

        bprev_pos = (50, 650)
        bnext_pos = (650, 650)
        bquit_pos = (675, 25)
        bsize = (100, 100)
        bprev = Button(bprev_pos, bsize, 'page_pos', images.BUTT_BCK_IMG,
                       None, None, ut.bfunc_cdec)
        bnext = Button(bnext_pos, bsize, 'page_pos', images.BUTT_NXT_IMG,
                       None, None, ut.bfunc_cinc)
        bquit = Button(bquit_pos, bsize, 'quit', images.BUTT_CLS_IMG,
                       None, None, ut.bfunc_cinc)

        htext_pos = (300, 650)
        htext_size = (400, 100)

        self.help_pages: List[List[GuiObject]] = []
        for x in range(4):
            tbox = TextBox(htext_pos, htext_size, str(x+1)+'/4', ut.GAME_FONT)
            self.help_pages.append([tbox])

        self.help_pages[0].extend(self.gen_first_help_page())

        lines = ['Основной игрок. Понятия не имеет, зачем ему эти монеты.',
                 'Зато умеет ходить и ставить бомбы, но откуда они у него?',
                 'Что он скрывает за своей улыбкой? Никто не знает...']
        self.help_pages[1].extend(self.gen_help_page(images.MAN_IMG[0], lines))

        img = images.MONEY_IMG[0]
        lines = ['Монетка, причём судя по всему шоколадная, т.к. боится огня.',
                 'Так как нужно собрать ВСЕ монетки, утрата одной означает',
                 'что вы уже проиграли. Обидно, да? А нечего взрывать всё!']
        self.help_pages[2].extend(self.gen_help_page(img, lines))

        lines = ['Череп нерадивого студента. Мечется по всему полю в поисках',
                 'преподавателя, чтобы досдать ему свой проект. Не вставайте',
                 'на его пути, а то зашибёт...и сдавайте дедлайны вовремя']
        img = images.ENEMY_IMG[1]
        self.help_pages[3].extend(self.gen_help_page(img, lines))

        self.title_box: TextBox = title_box
        self.button_prev: Button = bprev
        self.button_next: Button = bnext
        self.button_quit: Button = bquit

        triggers = [('page_pos', 0, len(self.help_pages)),
                    ('quit', 0, 2)]
        self.triggers: List[ut.Trigger] = triggers

    def gen_first_help_page(self) -> List[GuiObject]:
        line_pos = [(125, 225 + 50 * x) for x in range(8)]
        line_size = (550, 50)
        gui = []
        lines = ['Что, так и не понял, как тут всё работает? :)',
                 'Просто собери все монетки и победишь! Проще простого!',
                 'Стрелки - перемещение. Можно даже по диагонали.',
                 'Пробел - поставить бомбу, но только стоя на месте.',
                 'Цифры 3-7 - поставить таймер взрыва. Для ПРО',
                 'Для более подробного обзора - жамкай кнопку снизу',
                 'Если решил, что разберёшься сам - твоя кнопка сверху']

        for idx, line in enumerate(lines):
            gui.append(TextBox(line_pos[idx], line_size, line, ut.GAME_FONT))
        return gui

    def gen_help_page(self, img: ut.Image, lines) -> List[GuiObject]:
        gui = []
        char_pos = (300, 250)
        char_size = (200, 200)
        gui.append(FixedImage(char_pos, char_size, img))

        iline_pos = [(100, 470 + 50 * x) for x in range(4)]
        iline_size = (600, 50)
        for idx, line in enumerate(lines):
            line_tbox = TextBox(iline_pos[idx], iline_size, line, ut.GAME_FONT)
            gui.append(line_tbox)
        return gui

    def init(self, screen: ut.Image) -> None:
        """What to do when entering this mode"""
        self.back_img = screen.copy()

    def update_focus(self, mouse_pos: ut.Coord) -> None:
        """Calculate new focused GUI object, if possible"""
        gui_elems = [self.button_quit, self.button_prev, self.button_next]
        gui_triggers = [True, self.triggers[0][1] > 0,
                        self.triggers[0][1] < self.triggers[0][2]-1]
        if self.focused is not None:
            if gui_elems[self.focused].includes(mouse_pos) and \
               gui_triggers[self.focused]:
                return
            gui_elems[self.focused].focus = False
            self.focused = None

        focus_candidates: List[int] = []
        for idx in range(len(gui_elems)):
            if gui_elems[idx].includes(mouse_pos) and gui_triggers[idx]:
                focus_candidates.append(idx)

        # any sort of solving focus conflicts.. for example, first one
        if focus_candidates:
            self.focused = focus_candidates[0]
            gui_elems[self.focused].focus = True

    def main_loop(self, screen: ut.Image) -> bool:
        """Subsequently process all procedures for SplashScreen"""
        self.init(screen)
        while True:
            events = pygame.event.get()
            game_trigger = self.events(events, screen)

            self.draw(screen)
            pygame.display.flip()

            if self.triggers[1][1] == 1:
                self.leave()
                return True  # everything is okay, continue to work

            if not game_trigger:
                self.leave()
                return False  # time to go..

    def events(self, events: ut.Event,
               screen: ut.Image) -> bool:
        """Event parser: process all events from previous tick"""
        guis = [self.button_quit, self.button_prev, self.button_next]
        for event in events:
            if event.type is pygame.QUIT:
                dialog = CloseDialog()
                if dialog.main_loop(screen):
                    return False
            if event.type is pygame.MOUSEBUTTONDOWN:
                self.update_focus(event.pos)
                if self.focused is not None:
                    self.pressed_down = True
                    guis[self.focused].init_pdown(event.pos, self.triggers)

            elif event.type is pygame.MOUSEMOTION and self.pressed_down:
                if self.focused is not None:
                    guis[self.focused].next_pdown(event.pos, self.triggers)

            elif event.type is pygame.MOUSEBUTTONUP:
                if self.focused is not None:
                    guis[self.focused].init_pup(event.pos, self.triggers)
                    self.pressed_down = False
        return True

    def draw(self, screen: ut.Image) -> None:
        """Draw all GUI objects"""
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(self.back_img, (0, 0))
        screen.blit(self.menu_img, self.menu_pos)
        self.title_box.draw(screen, mouse_pos, self.triggers)

        for page_element in self.help_pages[self.triggers[0][1]]:
            page_element.draw(screen, mouse_pos, self.triggers)

        if self.triggers[0][1] > 0:
            self.button_prev.draw(screen, mouse_pos, self.triggers)
        if self.triggers[0][1] < self.triggers[0][2]-1:
            self.button_next.draw(screen, mouse_pos, self.triggers)
        self.button_quit.draw(screen, mouse_pos, self.triggers)

        screen.blit(self.cursor_img, mouse_pos)

    def leave(self) -> Optional[List[ut.Trigger]]:
        """What to do when leaving this mode"""
        return self.triggers
