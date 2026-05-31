# -*- coding: utf-8 -*-
"""
تبويب الملفات المستلمة
Files tab: list the files inside the shared folder (received from other devices)
and allow deleting them.
"""
import os

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IconLeftWidget, IconRightWidget, OneLineAvatarIconListItem


def _icon_for(name):
    ext = os.path.splitext(name)[1].lower()
    if ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"):
        return "image"
    if ext in (".mp4", ".mkv", ".avi", ".mov", ".webm"):
        return "video"
    if ext in (".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"):
        return "music"
    if ext in (".pdf",):
        return "file-pdf-box"
    if ext in (".zip", ".rar", ".7z", ".tar", ".gz"):
        return "folder-zip"
    if ext in (".doc", ".docx", ".txt", ".odt"):
        return "file-document"
    return "file"


class ReceiveTab(MDBoxLayout):
    """واجهة تبويب الملفات. القواعد معرفة في kv/receive.kv"""

    def on_kv_post(self, base_widget):
        self.refresh_text()
        self.refresh_list()

    def refresh_text(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        self.ids.files_title.text = app.tr("shared_files")
        self.ids.refresh_btn.text = app.tr("refresh")
        if app.server:
            self.ids.folder_value.text = app.server.shared_dir
        else:
            self.ids.folder_value.text = ""
        self.refresh_list()

    def refresh_list(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        container = self.ids.files_list
        container.clear_widgets()

        if not app.server:
            self.ids.empty_label.text = app.tr("no_files")
            self.ids.empty_label.opacity = 1
            return

        files = app.server.list_files()
        if not files:
            self.ids.empty_label.text = app.tr("no_files")
            self.ids.empty_label.opacity = 1
            return

        self.ids.empty_label.opacity = 0
        for name in files:
            item = OneLineAvatarIconListItem(text=name)
            item.add_widget(IconLeftWidget(icon=_icon_for(name)))
            del_icon = IconRightWidget(icon="delete")
            del_icon.bind(on_release=lambda w, n=name: self.delete(n))
            item.add_widget(del_icon)
            container.add_widget(item)

    def delete(self, name):
        app = MDApp.get_running_app()
        if not app.server:
            return
        if app.server.delete_file(name):
            app.toast(app.tr("deleted"))
        self.refresh_list()
