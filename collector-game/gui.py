"""
gui.py -- GUI submodule
=======================
This is module, which contains GUI Classes.
"""

import pygame  # type: ignore
import images
import utils as ut
from typing import List, Tuple, Optional


class GuiObject:
    """General entity of basic GUI object"""
    def __init__(self, pos: ut.Coord, size: ut.Size,
                 trigger_name: Optional[str] = None) -> None:
        """Initialise GUI object"""
        self.pos: ut.Coord = pos
        self.size: ut.Size = size
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
                 image_pressed: Optional[ut.Image] = None,
                 text: Optional[Tuple[str, str]] = None) -> None:
        """Initialise Button element"""
        super().__init__(pos, size, tname)

        self.image: ut.Image = pygame.transform.scale(image, size)
        self.image_pressed: Optional[ut.Image] = None
        if image_pressed:
            self.image_pressed = pygame.transform.scale(image_pressed, size)

        self.text: Optional[TextBox] = None
        if text:
            text_pos_x = int(pos[0] + 0.08*size[0])
            text_pos_y = int(pos[1] + 0.25*size[1])
            text_size = int(0.85*size[0]), int(0.8*size[1])
            self.text = TextBox((text_pos_x, text_pos_y), text_size, *text)

    def init_pdown(self, mouse_pos: ut.Coord,
                   triggers: Optional[List[ut.Trigger]] = None) -> None:
        """Process initial event of mouse key pressed down"""
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
                    triggers[t_idx] = tname, (tval+1) % tmax_val, tmax_val
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
        self.menu_pos: ut.Coord = menu_pos  # left upper corner
        self.cursor_img: ut.Image = images.CURSOR_IMG
        self.gui: Optional[List[GuiObject]] = gui
        self.focused: Optional[int] = None
        self.pressed_down: bool = False
        self.triggers: Optional[List[ut.Trigger]] = triggers

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

    def Events(self, events: List[ut.Event],
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

    def Draw(self, screen: ut.Image) -> None:
        """Draw all GUI objects"""
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(self.back_img, (0, 0))
        screen.blit(self.menu_img, self.menu_pos)
        if self.gui:
            for gui in self.gui:
                gui.draw(screen, mouse_pos, self.triggers)

        screen.blit(self.cursor_img, mouse_pos)

    def Leave(self) -> Optional[List[ut.Trigger]]:
        """What to do when leaving this mode"""
        pygame.mouse.set_visible(True)
        return self.triggers

    def Init(self, screen: ut.Image) -> None:
        """What to do when entering this mode"""
        pygame.mouse.set_visible(False)
        self.back_img = screen.copy()


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

    def MainLoop(self, screen: ut.Image) -> bool:
        """Subsequently process all procedures for CloseDialog"""
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

    def Events(self, events: List[ut.Event],
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

        menu_pos = pos_x+25, pos_y+400
        res_pos = pos_x+275, pos_y+400
        title_pos = pos_x, pos_y
        text1_pos = pos_x+50, pos_y+150
        text2_pos = pos_x+50, pos_y+300

        b_size = (200, 100)

        menu_text = ('МЕНЮ', ut.GAME_FONT)
        restart_text = ('ЗАНОВО', ut.GAME_FONT)
        menu = Button(menu_pos, b_size, 'menu', images.BUTT_TMP_IMG,
                      images.BUTT_TMP_PRESSED_IMG, menu_text)
        restart = Button(res_pos, b_size, 'restart', images.BUTT_TMP_IMG,
                         images.BUTT_TMP_PRESSED_IMG, restart_text)

        title_box = TextBox(title_pos, (500, 200), title_text, ut.GAME_FONT)
        text1_box = TextBox(text1_pos, (400, 100), text1, ut.GAME_FONT)
        text2_box = TextBox(text2_pos, (400, 100), text2, ut.GAME_FONT)

        my_gui = [title_box, text1_box, text2_box, menu, restart]
        self.gui: List[GuiObject] = my_gui

        triggers = [('restart', 0, 2), ('menu', 0, 2)]
        self.triggers: List[ut.Trigger] = triggers

    def MainLoop(self, screen: ut.Image) -> bool:
        """Subsequently process all procedures for SplashScreen"""
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

    def Events(self, events: ut.Event,
               screen: ut.Image) -> bool:
        """Event parser: process all events from previous tick"""
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
