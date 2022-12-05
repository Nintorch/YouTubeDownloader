import os
import webbrowser

import wx

import downloader
import ui

app_size = wx.Size(540, 720)
window_size = wx.Size(0, 0)  # will get properly set during initialization


# TODO: dark theme

def cropString(s, length):
    if len(s) < length:
        return s
    return s[:length] + "..."


def formatSize(size):
    if size < 1024:
        return f"{size} b"
    elif size < 1024 ** 2:
        return f"{size // 1024} kb"
    elif size < 1024 ** 3:
        return f"{size // 1024 ** 2} mb"
    else:
        return f"{size // 1024 ** 3} gb"


def uppercaseFormat(fmt: str):
    return fmt[1:].upper()


size_multipliers = {
    ".wav": 12
}


def output(s):
    parent = frame
    if frame.download_panel.IsShown():
        parent = frame.download_panel
    wx.MessageBox(s, "YouTubeDownloader", wx.OK, parent)
    frame.download_panel.SetCursor(ui.arrowCursor)


class DownloadPopup(wx.Frame):
    video_name: ui.TextLabel
    video_length: ui.TextLabel
    video_url: ui.TextLabel
    video_preview: ui.Image
    resolution: ui.SelectionVertical
    formats: ui.TextList
    sizes: ui.TextList
    filepath: ui.FilePath
    type_choose: ui.SelectionHorizontal
    format_choose: ui.DropDownList

    btn_close: ui.Image
    btn_download: ui.Button
    btn_cancel: ui.Button

    panel: wx.Panel
    video_details_panel: wx.Panel
    download_panel: wx.Panel
    resolution_panel: wx.Panel

    format = 0

    text_videourl = ""
    text_videoname = ""

    refresh = []

    data = None

    def __init__(self, parent, on_cancel, *args, **kw):
        super().__init__(parent, -1, pos=parent.GetPosition(), style=wx.CLOSE_BOX | wx.CAPTION, *args, **kw)
        self.SetClientSize(540, 583)

        global window_size
        window_size = self.GetSize()

        self.SetBackgroundColour(parent.GetBackgroundColour())
        self.refresh = []

        panel = self.panel = wx.Panel(self, -1, size=self.GetClientSize())
        self.refresh.append(panel)

        # Video details
        video_details = self.video_details_panel = wx.Panel(panel, -1, pos=wx.Point(0, 10), size=wx.Size(540, 70))
        self.refresh.append(video_details)
        self.video_name = ui.TextLabel(video_details, "(name placeholder)", wx.Point(138, 0), point_size=8)
        ui.Image(video_details, "images/access_time.png", wx.Point(138, 44))
        self.video_length = ui.TextLabel(video_details, "43:25", wx.Point(138 + 22, 41), point_size=2,
                                         color=wx.Colour(0x282524))
        ui.Image(video_details, "images/link.png", wx.Point(138 + 81, 44))
        self.video_url = ui.TextLabel(video_details, "(url placeholder)",
                                      wx.Point(138 + 81 + 20, 42),
                                      point_size=1, color=wx.Colour(0x5858F9), on_click=self._on_link_click)
        self.video_preview = ui.Image(video_details, "images/placeholder_preview.png", wx.Point(16, 0))

        # Video settings
        video_settings = wx.Panel(panel, -1, pos=wx.Point(16, 96), size=wx.Size(540 // 2, 94))
        self.refresh.append(video_settings)
        self.type_choose = ui.SelectionHorizontal(video_settings, ["Video + Audio", "Audio Only"],
                                                  wx.Point(0, 0), onclick=self._setup_formats)
        self.format_choose = ui.DropDownList(panel, "Format", [".mp4"], wx.Point(280 + 16, 7 + 96),
                                             wx.Size(96, 24), on_click=self._change_formats, align=ui.ALIGN_MIDDLE)

        # Select quality
        self.resolution_panel = resolution_panel = wx.Panel(panel, -1, pos=wx.Point(0, 162), size=wx.Size(540, 305))
        resolution_panel.SetBackgroundColour(self.GetBackgroundColour())
        self.refresh.append(resolution_panel)
        ui.TextLabel(resolution_panel, "Quality", wx.Point(30, 0),
                     point_size=1, color=wx.Colour(0x868180))
        self.resolution = ui.SelectionVertical(resolution_panel,
                                               ["2160p 4K"],
                                               wx.Point(30, 33), size=wx.Size(100, 80), elem_height=35)

        ui.TextLabel(resolution_panel, "Format", wx.Point(540 // 2, 0),
                     point_size=1, color=wx.Colour(0x868180), align=ui.ALIGN_MIDDLE)
        self.formats = ui.TextList(resolution_panel,
                                   ["MP4"],
                                   wx.Point(540 // 2 - 20, 33), size=wx.Size(40, 280), elem_height=35,
                                   align=ui.ALIGN_MIDDLE)

        ui.TextLabel(resolution_panel, "Size", wx.Point(540 - 45, 0),
                     point_size=1, color=wx.Colour(0x868180), align=ui.ALIGN_MIDDLE)
        self.sizes = ui.TextList(resolution_panel,
                                 ["~123.4 mb"],
                                 wx.Point(540 - 30 - 100, 33), size=wx.Size(100, 280), elem_height=35,
                                 align=ui.ALIGN_RIGHT)

        self.filepath = ui.FilePath(resolution_panel, wx.Point(16, self.resolution_panel.GetSize().y - 40),
                                    wx.Size(540 - 16 * 2, 32))

        # Download and cancel buttons
        download_panel = self.download_panel = wx.Panel(panel, -1, pos=wx.Point(320, panel.GetSize().y - 47),
                                                        size=wx.Size(204, 84))
        self.btn_download = ui.Button(download_panel, "Download", self._on_download_click, wx.Point(110, 0),
                                      ui.Button.SIZE_SMALL)
        self.btn_cancel = ui.Button(download_panel, "Cancel", on_cancel, wx.Point(0, 0),
                                    ui.Button.SIZE_SMALL, ui.Button.COLOR_DARK)

        self.Bind(wx.EVT_CLOSE, on_cancel)

        self._setup_formats()

    def update_data(self, url):
        data = downloader.get_video_details(url)
        if data:
            self.data = data

            self.text_videourl = url
            self.text_videoname = data["title"]

            self.video_url.SetText(cropString(url, 42))
            self.video_name.SetText(data["title"])
            if self.video_name.GetSize().x > 400:
                self.video_name.staticText.SetToolTip(data["title"])
                while self.video_name.GetSize().x > 390:
                    self.video_name.SetText(self.video_name.GetText()[:-1])
                self.video_name.SetText(self.video_name.GetText()[:-3] + "...")
            else:
                self.video_name.staticText.SetToolTip("")
            self.video_length.SetText(data["length"])

            size = max(len(data["video"]), len(data["audio"]))
            self.resolution_panel.SetSize(wx.Size(540, (size + 2) * self.resolution.elementHeight))
            self._update_resolutions(data)

            self.formats.SetChoices([uppercaseFormat(self.format_choose.choices[0])] * len(self.resolution))

            self.SetClientSize(wx.Size(540, 560 - (280 - size * self.resolution.elementHeight)))
            self.panel.SetSize(self.GetClientSize())
            self.download_panel.SetPosition(
                wx.Point(max(self.GetClientSize().x - 220, 0), max(self.panel.GetSize().y - 47, 0)))

            self.filepath.SetPosition(wx.Point(16, self.resolution_panel.GetSize().y - 40))

            self._update_thumbnail(data)

            return True
        else:
            frame.ShowError("Invalid YouTube video URL")
            return False

    def _on_download_click(self, _evt):
        stream: downloader.Stream
        audio_stream = None

        if self.filepath.path == "":
            output("Please provide a path")
            return
        elif os.path.exists(self.filepath.path):
            if wx.MessageBox("File already exists. Do you want to overwrite it?", "File already exists.",
                             wx.YES_NO | wx.CANCEL) != wx.YES:
                return
            os.remove(self.filepath.path)

        if self.type_choose.selected_id == 0:
            stream = self.data["video"][self.resolution.selected_id][0]
            if not stream.includes_audio_track:
                audio_stream = self.data["audio"][0][0]
        else:
            stream = self.data["audio"][self.resolution.selected_id][0]
        self.SetCursor(ui.hourglassCursor)
        downloader.stream_download(stream, audio_stream, self.filepath.path)

    def _on_link_click(self, _evt):
        webbrowser.open(self.text_videourl)

    def _setup_formats(self):
        if self.type_choose.selected_id == 0:
            formats = [".mp4", ".avi", ".mov", ".mkv"]
            self.format_choose.SetChoices(formats)
        else:
            formats = [".ogg", ".mp3", ".wav"]
            self.format_choose.SetChoices(formats)
        self._change_formats()

    def _change_formats(self):
        if self.data:
            self._update_resolutions(self.data)
        format = self.format_choose.choices[self.format_choose.selected_id]
        self.formats.SetChoices(
            [uppercaseFormat(format)] * len(self.resolution))

        if self.type_choose.selected_id == 0:
            self.filepath.wildcards = [f"{uppercaseFormat(format)} video (*{format})|*{format}"]
        else:
            self.filepath.wildcards = [f"{uppercaseFormat(format)} audio (*{format})|*{format}"]

        if self.filepath.path:
            self.filepath.SetPath(self.filepath.GetPath()[:-4] + format)

        self.Refresh()

    def _update_resolutions(self, data):
        format = self.format_choose.choices[self.format_choose.selected_id]
        if self.type_choose.selected_id == 0:
            self.resolution.SetChoices([x[1] for x in data["video"]])
            self.sizes.SetChoices(['~' + formatSize(size_multipliers.get(format, 1) * x[2]) for x in data["video"]])
        else:
            self.resolution.SetChoices([x[1] for x in data["audio"]])
            self.sizes.SetChoices(['~' + formatSize(size_multipliers.get(format, 1) * x[2]) for x in data["audio"]])

    def _update_thumbnail(self, data):
        image = wx.Image(data["thumbnail"])

        image_size = image.GetSize()
        cropped = image.GetSubImage(wx.Rect(0, int(image_size.y*0.125), image_size.x, int(image_size.y*0.75)))
        image.Destroy()

        scaled = cropped.Scale(106, 60)
        cropped.Destroy()

        self.video_preview.SetImage(scaled)

        os.remove(data["thumbnail"])


class MainFrame(wx.Frame):
    url: ui.TextEdit
    copyPasteText: ui.TextLabel
    errorText: ui.TextLabel
    btnDownload: ui.Button
    btnPasteLink: ui.Button
    formatSelection: ui.SelectionVertical

    github: ui.Image
    website: ui.Image

    panel: wx.Panel
    download_panel: DownloadPopup

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.SetClientSize(app_size)
        self.Center()
        self.SetBackgroundColour(wx.Colour(243, 243, 243))
        self.SetMinSize(wx.Size(300, 340))

        ui.Init()

        self.panel = wx.Panel(self, -1, size=app_size)

        self.download_panel = DownloadPopup(self, self.OnCancelClick)
        self.download_panel.Hide()

        self.copyPasteText = ui.TextLabel(self.panel, "Copy and paste the link to get started",
                                          position=wx.Point(app_size.x // 2, 276),
                                          point_size=1)
        xsize = self.copyPasteText.GetSize().x
        self.copyPasteText.SetPosition(wx.Point(app_size.x // 2 - xsize // 2, 276))

        self.errorText = ui.TextLabel(self.panel, "",
                                      position=wx.Point(0, 400),
                                      point_size=3, color=wx.RED)

        self.btnDownload = ui.Button(self.panel, "Download", self.OnDownloadClick,
                                     wx.Point(app_size.x // 2 - 73, app_size.y // 2 - 32),
                                     point_size=7)
        self.btnPasteLink = ui.Button(self.panel, "+ Paste link", self.OnDownloadClick, wx.Point(16, 14),
                                      size=ui.Button.SIZE_MEDIUM)

        self.github = ui.Image(self.panel, "images/github.png", wx.Point(44, 696), on_click=self.OnGitHubClick)
        self.website = ui.Image(self.panel, "images/website.png", wx.Point(16, 696), on_click=self.OnWebsiteClick)

        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnDownloadClick(self, _evt):
        text_data = wx.TextDataObject()
        success = False
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(text_data)
            wx.TheClipboard.Close()
        if success:
            self.SetCursor(ui.hourglassCursor)
            self.HideError()
            if self.download_panel.update_data(text_data.GetText()):
                self.Disable()
                self.download_panel.SetPosition(wx.Point(self.GetPosition().x, self.GetPosition().y +
                                                         (app_size.y // 2 - self.download_panel.GetSize().y // 2)))
                self.download_panel.Show()
                self.download_panel.Raise()
            self.SetCursor(ui.arrowCursor)
        else:
            self.ShowError("Error getting text from clipboard")
            return

    def OnCancelClick(self, _evt):
        self.Enable()
        self.download_panel.Hide()

    def OnGitHubClick(self, _evt):
        webbrowser.open("https://github.com/JustMeCodes/YoutubeDownloader")

    def OnWebsiteClick(self, _evt):
        webbrowser.open("example.com")

    def ShowError(self, text):
        self.errorText.SetText(text)
        xsize = self.errorText.GetSize().x
        self.errorText.SetPosition(wx.Point(app_size.x // 2 - xsize // 2, app_size.y // 2 + 50))

    def HideError(self):
        self.errorText.SetText("")

    def OnResize(self, _evt: wx.SizeEvent):
        global app_size
        app_size = self.GetClientSize()

        self.panel.SetSize(app_size)

        xsize = self.copyPasteText.GetSize().x
        self.copyPasteText.SetPosition(wx.Point(app_size.x // 2 - xsize // 2, app_size.y // 2 - 84))
        xsize = self.errorText.GetSize().x
        self.errorText.SetPosition(wx.Point(app_size.x // 2 - xsize // 2, app_size.y // 2 + 50))

        self.btnDownload.SetPosition(wx.Point(app_size.x // 2 - 73, app_size.y // 2 - 32))

        self.github.SetPosition(wx.Point(44, app_size.y - 24))
        self.website.SetPosition(wx.Point(16, app_size.y - 24))

        self.Refresh()


downloader.output = output

app = wx.App()
frame = MainFrame(None, title="YouTube Downloader")
frame.Show()
app.MainLoop()
