# -*- coding: utf-8 -*-
import os
import threading

from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import IconLeftWidget, OneLineAvatarIconListItem

from app.ftp_client import upload_files

ACCENT = get_color_from_hex("#00d4aa")


def _icon_for(name):
    ext = os.path.splitext(name)[1].lower()
    if ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"): return "image"
    if ext in (".mp4", ".mkv", ".avi", ".mov", ".webm"):          return "video"
    if ext in (".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"): return "music"
    if ext == ".pdf":                                              return "file-pdf-box"
    if ext in (".zip", ".rar", ".7z", ".tar", ".gz"):             return "folder-zip"
    if ext in (".doc", ".docx", ".txt", ".odt"):                  return "file-document"
    return "file-outline"


class SendTab(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = []
        self.file_manager = None

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.refresh_text(), 0)

    def _get_file_manager(self):
        if self.file_manager is None:
            self.file_manager = MDFileManager(
                exit_manager=self._exit_manager,
                select_path=self._select_path,
                selector="multi",
            )
        return self.file_manager

    def refresh_text(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        self.ids.connect_title.text  = app.tr("connect_title").upper()
        self.ids.host_field.hint_text = app.tr("host_ip")
        self.ids.port_field.hint_text = app.tr("host_port")
        self.ids.pick_label.text     = app.tr("pick_files")
        self.ids.send_btn.text       = app.tr("send_files")
        self.ids.selected_title.text = app.tr("selected_files").upper()
        self._update_list()

    def open_file_manager(self):
        start = os.path.expanduser("~")
        if not os.path.isdir(start):
            start = "/"
        self._get_file_manager().show(start)

    def _select_path(self, path):
        if isinstance(path, (list, tuple)):
            for p in path:
                if os.path.isfile(p) and p not in self.selected:
                    self.selected.append(p)
        else:
            if os.path.isfile(path) and path not in self.selected:
                self.selected.append(path)
        self._exit_manager()
        self._update_list()

    def _exit_manager(self, *args):
        if self.file_manager:
            self.file_manager.close()

    def _update_list(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        container = self.ids.selection_list
        container.clear_widgets()
        count = len(self.selected)
        self.ids.file_count_label.text = f"  {count}" if count else ""
        for path in self.selected:
            name = os.path.basename(path)
            item = OneLineAvatarIconListItem(
                text=name,
                theme_text_color="Custom",
                text_color=get_color_from_hex("#8892b0"),
                bg_color=get_color_from_hex("#22263a"),
            )
            item.add_widget(IconLeftWidget(
                icon=_icon_for(name),
                theme_text_color="Custom",
                text_color=ACCENT,
            ))
            container.add_widget(item)

    def send(self):
        app = MDApp.get_running_app()
        host = self.ids.host_field.text.strip()
        port = self.ids.port_field.text.strip() or "2121"
        if not host:
            app.toast(app.tr("enter_ip")); return
        if not self.selected:
            app.toast(app.tr("no_selection")); return
        app.toast(app.tr("sending"))
        self.ids.send_progress.opacity = 1
        self.ids.send_progress.value   = 0
        self.ids.send_btn.disabled     = True
        files = list(self.selected)
        total = len(files)

        def _progress(idx, tot, name):
            Clock.schedule_once(
                lambda dt: setattr(self.ids.send_progress, "value", idx / tot * 100)
            )

        threading.Thread(
            target=self._do_upload,
            args=(host, port, files, _progress),
            daemon=True,
        ).start()

    def _do_upload(self, host, port, files, progress_cb):
        app = MDApp.get_running_app()
        try:
            success, errors = upload_files(host, port, files, progress_cb)
            if errors and success == 0:
                Clock.schedule_once(lambda dt: app.toast(app.tr("send_failed")))
            else:
                Clock.schedule_once(lambda dt: self._on_sent())
        except Exception:
            Clock.schedule_once(lambda dt: app.toast(app.tr("connect_failed")))
        finally:
            Clock.schedule_once(lambda dt: self._reset_progress())

    def _on_sent(self):
        MDApp.get_running_app().toast(MDApp.get_running_app().tr("send_success"))
        self.selected = []
        self._update_list()

    def _reset_progress(self):
        if not self.ids: return
        self.ids.send_progress.opacity = 0
        self.ids.send_progress.value   = 0
        self.ids.send_btn.disabled     = False
