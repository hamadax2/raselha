# -*- coding: utf-8 -*-
import os

from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IconLeftWidget, IconRightWidget, OneLineAvatarIconListItem

ACCENT = get_color_from_hex("#00d4aa")
DANGER = get_color_from_hex("#ff4d6d")


def _icon_for(name):
    ext = os.path.splitext(name)[1].lower()
    if ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"): return "image"
    if ext in (".mp4", ".mkv", ".avi", ".mov", ".webm"):          return "video"
    if ext in (".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"): return "music"
    if ext == ".pdf":                                              return "file-pdf-box"
    if ext in (".zip", ".rar", ".7z", ".tar", ".gz"):             return "folder-zip"
    if ext in (".doc", ".docx", ".txt", ".odt"):                  return "file-document"
    return "file-outline"


class ReceiveTab(MDBoxLayout):

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self._init(), 0)

    def _init(self):
        self.refresh_text()
        self.refresh_list()

    def refresh_text(self):
        app = MDApp.get_running_app()
        if not self.ids: return
        self.ids.files_title.text  = app.tr("shared_files").upper()
        self.ids.folder_value.text = app.server.shared_dir

    def refresh_list(self):
        app = MDApp.get_running_app()
        if not self.ids: return
        container = self.ids.files_list
        container.clear_widgets()
        files = app.server.list_files()
        count = len(files)
        self.ids.file_count_badge.text = str(count) if count else ""
        if not files:
            self.ids.empty_label.opacity = 1
            self.ids.empty_label.text    = app.tr("no_files")
            return
        self.ids.empty_label.opacity = 0
        for name in files:
            item = OneLineAvatarIconListItem(
                text=name,
                theme_text_color="Custom",
                text_color=get_color_from_hex("#8892b0"),
                bg_color=get_color_from_hex("#22263a"),
            )
            left  = IconLeftWidget(icon=_icon_for(name), theme_text_color="Custom", text_color=ACCENT)
            right = IconRightWidget(icon="delete-outline", theme_text_color="Custom", text_color=DANGER)
            right.bind(on_release=lambda w, n=name: self.delete(n))
            item.add_widget(left)
            item.add_widget(right)
            container.add_widget(item)

    def delete(self, name):
        app = MDApp.get_running_app()
        if app.server.delete_file(name):
            app.toast(app.tr("deleted"))
        self.refresh_list()
