import os
import sys

import wx
import wx.lib.agw.artmanager

from typing import Dict, List, Callable

am: wx.lib.agw.artmanager.ArtManager
handCursor: wx.Cursor
arrowCursor: wx.Cursor
hourglassCursor: wx.Cursor

ALIGN_LEFT = 0
ALIGN_MIDDLE = 1
ALIGN_RIGHT = 2


def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, path)


class Clickable:
    onClick: None
    pressed = False

    def _setup_clickable(self, element):
        element.SetCursor(handCursor)
        element.Bind(wx.EVT_LEFT_DOWN, self._on_down)
        element.Bind(wx.EVT_LEFT_UP, self._on_up)
        element.Bind(wx.EVT_LEAVE_WINDOW, self._on_leave)

    def _on_down(self, _evt):
        self.pressed = True

    def _on_up(self, evt):
        if self.pressed:
            self.onClick(evt)
        self.pressed = False

    def _on_leave(self, _evt):
        self.pressed = False


class TextLabel(Clickable):
    staticText: wx.StaticText

    def __init__(self, parent, text: str, position: wx.Point, size: wx.Size = None, color: wx.Colour = wx.BLACK,
                 on_click=None, point_size=3, align=ALIGN_LEFT):
        if not size:
            size = wx.DefaultSize
        self.staticText = wx.StaticText(parent, -1, text, pos=position, size=size)
        if align == ALIGN_MIDDLE:
            position.x -= self.staticText.GetSize().x // 2
            self.staticText.SetPosition(position)
        elif align == ALIGN_RIGHT:
            position.x -= self.staticText.GetSize().x
            self.staticText.SetPosition(position)

        font = self.staticText.GetFont()
        font.PointSize += point_size
        self.staticText.SetFont(font)
        self.staticText.SetForegroundColour(color)

        if on_click:
            self.onClick = on_click
            super()._setup_clickable(self.staticText)

    def SetText(self, text: str):
        self.staticText.SetLabelText(text)

    def GetText(self):
        return self.staticText.GetLabelText()

    def GetPosition(self) -> wx.Point:
        return self.staticText.GetPosition()

    def SetPosition(self, pos: wx.Point):
        self.staticText.SetPosition(pos)

    def GetSize(self) -> wx.Size:
        return self.staticText.GetSize()


class Image(Clickable):
    staticBitmap: wx.StaticBitmap

    def __init__(self, parent, path: str, position: wx.Point, on_click=None):
        self.staticBitmap = wx.StaticBitmap(parent, -1, wx.Bitmap(resource_path(path)), pos=position)

        if on_click:
            self.onClick = on_click
            super()._setup_clickable(self.staticBitmap)

    def SetPosition(self, position: wx.Point):
        self.staticBitmap.SetPosition(position)

    def SetImage(self, image: wx.Image):
        self.staticBitmap.SetBitmap(image.ConvertToBitmap())
        self.staticBitmap.Refresh()

    def SetBitmap(self, bitmap: wx.Bitmap):
        self.staticBitmap.SetBitmap(bitmap)
        self.staticBitmap.Refresh()


class TextEdit:
    textCtrl: wx.TextCtrl

    def __init__(self, parent, placeholder: str, position: wx.Point, size: wx.Size = None, point_size=3):
        if not size:
            size = wx.DefaultSize
        self.textCtrl = wx.TextCtrl(parent, -1, placeholder, pos=position, size=size)
        font = self.textCtrl.GetFont()
        font.PointSize += point_size
        self.textCtrl.SetFont(font)

    def SetText(self, text: str):
        self.textCtrl.SetLabelText(text)


_buttonImagesLarge = {
    "normal": None,
    "hover": None,
    "shadow": None,
    "offsetx": 0,
    "offsety": 0,
}

_buttonImagesMedium = {
    "normal": None,
    "hover": None,
    "shadow": None,
    "offsetx": 0,
    "offsety": 0,
}

_buttonImagesSmall = {
    "normal": None,
    "hover": None,
    "shadow": None,
    "offsetx": 0,
    "offsety": 0,
}

_buttonImagesSmallDark = {
    "normal": None,
    "hover": None,
    "shadow": None,
    "offsetx": 0,
    "offsety": 0,
}

_buttonImagesFilePath = {
    "normal": None,
    "hover": None,
    "shadow": None,
    "offsetx": 0,
    "offsety": 0,
}


class Button:
    # Enums
    # Size
    SIZE_LARGE = 0
    SIZE_MEDIUM = 1
    SIZE_SMALL = 2

    # Color
    COLOR_NORMAL = 0
    COLOR_DARK = 1

    ui: wx.StaticBitmap
    shadow: wx.StaticBitmap
    image: wx.Bitmap

    onclick = None
    pressed = False
    text = ""

    size = wx.Size()

    pointSize = 0

    _buttonImages = _buttonImagesLarge
    _offsetx = 0
    _offsety = 0

    @staticmethod
    def init_images():
        _buttonImagesLarge["normal"] = wx.Bitmap(resource_path("images/button_large.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesLarge["hover"] = wx.Bitmap(resource_path("images/button_large_hover.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesLarge["shadow"] = wx.Bitmap(resource_path("images/button_large_shadow.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesLarge["offsetx"] = 24
        _buttonImagesLarge["offsety"] = 16
        _buttonImagesMedium["normal"] = wx.Bitmap(resource_path("images/button_medium.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesMedium["hover"] = wx.Bitmap(resource_path("images/button_medium_hover.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesMedium["offsetx"] = 0
        _buttonImagesMedium["offsety"] = 0
        _buttonImagesSmall["normal"] = wx.Bitmap(resource_path("images/button_small.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesSmall["hover"] = wx.Bitmap(resource_path("images/button_small_hover.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesSmall["offsetx"] = 0
        _buttonImagesSmall["offsety"] = 0
        _buttonImagesSmallDark["normal"] = wx.Bitmap(resource_path("images/button_small_gray.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesSmallDark["hover"] = wx.Bitmap(resource_path("images/button_small_gray_hover.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesSmallDark["offsetx"] = 0
        _buttonImagesSmallDark["offsety"] = 0
        _buttonImagesFilePath["normal"] = wx.Bitmap(resource_path("images/button_file_dialog.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesFilePath["hover"] = wx.Bitmap(resource_path("images/button_file_dialog_hover.png"), wx.BITMAP_TYPE_PNG)
        _buttonImagesFilePath["offsetx"] = 0
        _buttonImagesFilePath["offsety"] = 0

    def __init__(self, parent, text: str, onclick, position: wx.Point, size=SIZE_LARGE, color=COLOR_NORMAL,
                 point_size=3):
        if size == Button.SIZE_SMALL:
            if color == Button.COLOR_DARK:
                self._buttonImages = _buttonImagesSmallDark
            else:
                self._buttonImages = _buttonImagesSmall
        elif size == Button.SIZE_MEDIUM:
            self._buttonImages = _buttonImagesMedium
        elif size == 3:
            self._buttonImages = _buttonImagesFilePath

        self.image = self._buttonImages["normal"]
        self.onclick = onclick
        self.text = text
        self.pointSize = point_size

        # position.x -= self._buttonImages["offsetx"]
        # position.y -= self._buttonImages["offsety"]

        self._offsetx = self._buttonImages["offsetx"]
        self._offsety = self._buttonImages["offsety"]

        self.shadow = None
        if self._buttonImages["shadow"]:
            self.shadow = wx.StaticBitmap(parent, -1, self._buttonImages["shadow"],
                                          pos=wx.Point(position.x - self._buttonImages["offsetx"],
                                                       position.y - self._buttonImages["offsety"]))
            parent = self.shadow
            position = wx.Point(self._offsetx, self._offsety)
        self.ui = wx.StaticBitmap(parent, -1, self._buttonImages["normal"],
                                  pos=position)
        self.ui.SetCursor(handCursor)
        self.ui.Bind(wx.EVT_LEFT_DOWN, self._on_down)
        self.ui.Bind(wx.EVT_LEFT_UP, self._on_up)
        self.ui.Bind(wx.EVT_ENTER_WINDOW, self._on_enter)
        self.ui.Bind(wx.EVT_LEAVE_WINDOW, self._on_leave)
        self.ui.Bind(wx.EVT_PAINT, self._on_paint)

    def SetPosition(self, position: wx.Point):
        if self.shadow:
            self.shadow.SetPosition(wx.Point(position.x - self._offsetx, position.y - self._offsety))
        else:
            self.ui.SetPosition(position)

    def SetImages(self, images):
        self._buttonImages = images

    def _on_down(self, _evt):
        self.pressed = True
        self.image = self._buttonImages["normal"]
        self._refresh()

    def _on_up(self, evt):
        if self.pressed:
            self.onclick(evt)
            self.image = self._buttonImages["hover"]
            self._refresh()
        self.pressed = False

    def _on_enter(self, _evt):
        self.image = self._buttonImages["hover"]
        self._refresh()

    def _on_leave(self, _evt):
        self.pressed = False
        self.image = self._buttonImages["normal"]
        self._refresh()

    def _on_paint(self, _evt):
        if not self.ui:
            return
        dc = wx.PaintDC(self.ui)
        # TODO: Draw a rounded rectangle instead of different images using dc.DrawRoundedRectangle with
        #  wx.GraphicsContext
        dc.DrawBitmap(self.image, 0, 0)

        font = dc.GetFont()
        font.PointSize += self.pointSize
        dc.SetFont(font)
        text_size = dc.GetTextExtent(self.text)
        dc.SetTextForeground(wx.WHITE)

        dc.DrawText(self.text, self.ui.Size.x // 2 - text_size.x // 2, self.ui.Size.y // 2 - text_size.y // 2 - 1)

    def _refresh(self):
        if self.shadow and self.shadow.Enabled:
            self.shadow.Refresh()
        elif self.ui.Enabled:
            self.ui.Refresh()


_select_images: Dict[str, wx.Bitmap] = {
    "off": None,
    "on": None
}


class SelectionHorizontal(wx.Window):
    selected_id = 0
    choices = []
    parent: wx.Frame
    pointSize = 0
    elementWidth = 0
    click_event = None

    def __init__(self, parent, choices: List[str], position: wx.Point, point_size=3, onclick=None,
                 *args, **kw):
        super().__init__(parent, -1, pos=position, size=wx.Size(10, 10), *args, **kw)

        self.parent = parent
        self.choices = choices
        self.pointSize = point_size
        if onclick:
            self.click_event = onclick
        else:
            self.click_event = lambda: None

        dc = wx.ScreenDC()
        self.font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        dc.SetFont(self.font)
        maxWidth = 0
        for ch in self.choices:
            width = dc.GetTextExtent(ch).x
            if width > maxWidth:
                maxWidth = width

        self.elementWidth = maxWidth + 15
        self.SetSize(wx.Size(self.elementWidth * len(choices) + 8, 34))

        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_click)

    def _on_paint(self, _evt):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        gc: wx.GraphicsContext

        gc.SetPen(wx.TRANSPARENT_PEN)
        gc.SetBrush(wx.WHITE_BRUSH)
        gc.DrawRoundedRectangle(0, 0, self.GetSize().x, 34, 17)
        gc.SetBrush(wx.Brush(wx.Colour(249, 88, 88)))

        for i in range(len(self.choices)):
            if i == self.selected_id:
                gc.SetFont(self.font, wx.WHITE)
                gc.DrawRoundedRectangle(4 + self.elementWidth * i, 3, self.elementWidth, 28, 14)
            else:
                gc.SetFont(self.font, wx.Colour(0x868180))

            size = gc.GetFullTextExtent(self.choices[i])
            gc.DrawText(self.choices[i], 6 + self.elementWidth * (i + 0.5) - size[0] / 2, size[1]/2-2)

    def _on_click(self, evt):
        i = (evt.GetLogicalPosition(wx.ClientDC(self)).x-4)//self.elementWidth
        if 0 <= i < len(self.choices):
            self.Select(i)

    def __len__(self):
        return len(self.choices)

    def Select(self, i):
        self.selected_id = i
        self.Refresh()
        self.click_event()


class SelectionVertical(wx.Window):
    selected_id = 0
    choices = []
    parent: wx.Frame
    pointSize = 0
    elementHeight = 0
    click_event = None

    _brush: wx.Brush

    @staticmethod
    def init_images():
        _select_images["off"] = wx.Bitmap(resource_path("images/checkbox.png"), wx.BITMAP_TYPE_PNG)
        _select_images["on"] = wx.Bitmap(resource_path("images/checkbox_selected.png"), wx.BITMAP_TYPE_PNG)

    def __init__(self, parent, choices: List[str], position: wx.Point, size: wx.Size, point_size=3, elem_height=0,
                 onclick=None, *args, **kw):

        super().__init__(parent, -1, pos=position, size=size, *args, **kw)

        self.parent = parent
        self.choices = choices
        self.pointSize = point_size
        if elem_height <= 0:
            elem_height = point_size + 20
        self.elementHeight = elem_height
        if onclick:
            self.click_event = onclick
        else:
            self.click_event = lambda: None
        self._brush = wx.Brush(self.parent.GetBackgroundColour())

        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_click)
        self.Bind(wx.EVT_MOTION, self._on_motion)

    def _on_paint(self, _evt):
        dc = wx.PaintDC(self)

        dc.SetBackground(self._brush)
        dc.Clear()

        font = dc.GetFont()
        font.PointSize += self.pointSize
        dc.SetFont(font)

        for i in range(len(self.choices)):
            y = i * self.elementHeight
            dc.DrawBitmap(_select_images["on" if self.selected_id == i else "off"], 0, y)
            dc.DrawText(self.choices[i], 25, y - 4)

    def _on_click(self, evt):
        y = evt.GetLogicalPosition(wx.ClientDC(self)).y
        if y % self.elementHeight > (self.pointSize + 15):
            return
        self.Select(y // self.elementHeight)

    def _on_motion(self, evt: wx.MouseEvent):
        y = evt.GetPosition().y
        if y % self.elementHeight > (self.pointSize + 15):
            self.SetCursor(arrowCursor)
        else:
            self.SetCursor(handCursor)

    def __len__(self):
        return len(self.choices)

    def SetChoices(self, choices: List[str]):
        self.selected_id = 0
        self.choices = choices
        self.SetSize(wx.Size(self.GetSize().x, len(choices) * self.elementHeight))
        self.Refresh()

    def Select(self, i):
        self.selected_id = i
        self.Refresh()
        self.click_event()


class TextList(wx.Window):
    choices = []
    parent: wx.Frame
    pointSize = 0
    elementHeight = 0

    size: wx.Size
    align = 0

    _brush: wx.Brush

    def __init__(self, parent, choices: List[str], position: wx.Point, size: wx.Size, point_size=3, elem_height=0,
                 align=ALIGN_LEFT, *args, **kw):

        super().__init__(parent, -1, pos=position, size=size, *args, **kw)

        self.parent = parent
        self.choices = choices
        self.pointSize = point_size
        if elem_height <= 0:
            elem_height = point_size + 20
        self.elementHeight = elem_height
        self.size = size
        self.align = align
        self._brush = wx.Brush(self.parent.GetBackgroundColour())

        self.Bind(wx.EVT_PAINT, self._on_paint)

    def _on_paint(self, _evt):
        dc = wx.PaintDC(self)

        dc.SetBackground(self._brush)
        dc.Clear()

        font = dc.GetFont()
        font.PointSize += self.pointSize
        dc.SetFont(font)

        for i in range(len(self.choices)):
            y = i * self.elementHeight
            if self.align == ALIGN_LEFT:
                dc.DrawText(self.choices[i], 0, y - 4)
            elif self.align == ALIGN_MIDDLE:
                xsize = dc.GetFullTextExtent(self.choices[i], font)[0]
                dc.DrawText(self.choices[i], self.size.x // 2 - xsize // 2, y - 4)
            elif self.align == ALIGN_RIGHT:
                xsize = dc.GetFullTextExtent(self.choices[i], font)[0]
                dc.DrawText(self.choices[i], self.size.x - xsize, y - 4)

    def SetChoices(self, choices: List[str]):
        self.choices = choices
        self.SetSize(wx.Size(self.GetSize().x, len(choices) * self.elementHeight))
        self.Refresh()


_drop_down_arrow = None


class DropDownList(wx.Window, Clickable):
    selected_id = 0
    choices = []
    parent: wx.Frame
    pointSize = 0
    elementHeight = 0
    label = ""

    size: wx.Size
    initial_size: wx.Size
    align = 0

    opened = False

    _brush: wx.Brush

    click_event = None

    @staticmethod
    def init_images():
        global _drop_down_arrow
        _drop_down_arrow = wx.Bitmap(resource_path("images/drop_down_arrow.png"), wx.BITMAP_TYPE_PNG)

    def __init__(self, parent, label: str, choices: List[str], position: wx.Point, size: wx.Size, point_size=3,
                 align=ALIGN_LEFT, on_click=Callable[[int], None], *args, **kw):

        super().__init__(parent, -1, pos=position, size=size, *args, **kw)

        self.parent = parent
        self.choices = choices
        self.pointSize = point_size
        self.size = self.initial_size = size
        self.elementHeight = size.y
        self.align = align
        self.label = label
        self.click_event = on_click

        self._brush = wx.Brush(self.parent.GetBackgroundColour())

        self.onClick = self.OnClick
        self._setup_clickable(self)
        self.Bind(wx.EVT_PAINT, self._on_paint)

    def _on_paint(self, _evt):
        dc = wx.PaintDC(self)

        dc.SetBackground(self._brush)
        dc.Clear()

        font = dc.GetFont()
        font.PointSize += self.pointSize
        dc.SetFont(font)

        self._draw_text(dc, self.label, font, self.initial_size.y // 2 - self.pointSize - 8, draw_arrow=True)

        if self.opened:
            for i in range(len(self.choices)):
                y = int(self.initial_size.y * (i + 1.5)) - self.pointSize - 8
                self._draw_text(dc, self.choices[i], font, int(y))

    def _draw_text(self, dc: wx.DC, text, font, y, draw_arrow=False):
        if self.align == ALIGN_LEFT:
            xsize = dc.GetFullTextExtent(text, font)[0]
            dc.DrawText(text, 0, y)
            if draw_arrow:
                dc.DrawBitmap(_drop_down_arrow, xsize+6, y+9)
        elif self.align == ALIGN_MIDDLE:
            xsize = dc.GetFullTextExtent(text, font)[0]
            dc.DrawText(text, self.size.x // 2 - xsize // 2, y)
            if draw_arrow:
                dc.DrawBitmap(_drop_down_arrow, self.size.x // 2 + xsize // 2 + 6, y+9)
        elif self.align == ALIGN_RIGHT:
            xsize = dc.GetFullTextExtent(text, font)[0]
            if draw_arrow:
                dc.DrawText(text, self.size.x - xsize - 16, y)
                dc.DrawBitmap(_drop_down_arrow, self.size.x - 16, y+9)
            else:
                dc.DrawText(text, self.size.x - xsize, y)

    def SetChoices(self, choices: List[str]):
        self.choices = choices
        self.selected_id = 0
        if self.opened:
            self.size.y = self.initial_size.y
            self.SetSize(self.size)
            self.opened = False
        self.Refresh()

    def OnClick(self, evt: wx.MouseEvent):
        if not self.opened:
            self.size = wx.Size(self.initial_size)
            self.size.y *= len(self.choices) + 1
            self.SetSize(self.size)
            self.Refresh()
            self.opened = True
        elif evt.GetPosition().y < self.initial_size.y:
            self.size.y = self.initial_size.y
            self.SetSize(self.size)
            self.Refresh()
            self.opened = False
            self.click_event()
        else:
            self.selected_id = (evt.GetPosition().y-self.initial_size.y)//self.initial_size.y
            self.size.y = self.initial_size.y
            self.SetSize(self.size)
            self.Refresh()
            self.opened = False
            self.click_event()

    def Select(self, i):
        self.selected_id = i
        self.Refresh()


class FilePath(wx.Window):
    button: Button
    textctrl: wx.TextCtrl

    path = ""

    wildcards = None

    def __init__(self, parent, position: wx.Point, size: wx.Size, point_size=3, align=ALIGN_LEFT, *args, **kw):
        super().__init__(parent, -1, pos=position, size=size, *args, **kw)

        self.wildcards = []
        xsize = _buttonImagesFilePath["normal"].GetSize().x
        ysize = _buttonImagesFilePath["normal"].GetSize().y
        self.button = Button(self, "", self.OnButtonClick, wx.Point(size.x - xsize, 0), size=3)
        self.textctrl = wx.TextCtrl(self, -1, size=wx.Size(size.x - xsize - 10, ysize))

    def OnButtonClick(self, _evt):
        with wx.FileDialog(self, "Choose an output file", "", "",
                           '|'.join(self.wildcards), wx.FD_SAVE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.path = dlg.GetPath()
                self.textctrl.SetLabelText(self.path)

    def SetPath(self, path):
        self.path = path
        self.textctrl.SetLabelText(path)
        self.Refresh()

    def GetPath(self):
        return self.path


def Init():
    global am
    global handCursor
    global arrowCursor
    global hourglassCursor
    am = wx.lib.agw.artmanager.ArtManager()
    am.Initialize()
    Button.init_images()
    SelectionVertical.init_images()
    DropDownList.init_images()
    handCursor = wx.Cursor(wx.CURSOR_HAND)
    arrowCursor = wx.Cursor(wx.CURSOR_ARROW)
    hourglassCursor = wx.Cursor(wx.HOURGLASS_CURSOR)
