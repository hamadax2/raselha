# -*- coding: utf-8 -*-
"""
تبويب الإرسال
Send tab: pick files with MDFileManager then upload them to another device's
FTP server over the Hotspot network.
"""
import os
import threading

from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from app.ftp_client import upload_files


class SendTab(MDBoxLayout):
    """واجهة تبويب الإرسال. القواعد معرفة في kv/send.kv"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = []
        self.file_manager = MDFileManager(
            exit_manager=self._exit_manager,
            select_path=self._select_path,
            selector="multi",
        )

    def on_kv_post(self, base_widget):
        self.refresh_text()

    def refresh_text(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        self.ids.connect_title.text = app.tr("connect_title")
        self.ids.host_field.hint_text = app.tr("host_ip")
        self.ids.port_field.hint_text = app.tr("host_port")
        self.ids.pick_btn.text = app.tr("pick_files")
        self.ids.send_btn.text = app.tr("send_files")
        self.ids.selected_title.text = app.tr("selected_files")
        self._update_selection_label()

    # ------- اختيار الملفات -------
    def open_file_manager(self):
        from kivy.utils import platform
        if platform == "android":
            try:
                # Use app's internal storage as starting point on Android
                from android.storage import app_storage_path
                start = app_storage_path()
            except Exception:
                start = "/sdcard"
        else:
            start = os.path.expanduser("~")
        
        if not os.path.isdir(start):
            start = "/"
        self.file_manager.show(start)

    def _select_path(self, path):
        # في وضع multi قد تأتي قائمة أو مسار واحد
        if isinstance(path, (list, tuple)):
            for p in path:
                if os.path.isfile(p) and p not in self.selected:
                    self.selected.append(p)
        else:
            if os.path.isfile(path) and path not in self.selected:
                self.selected.append(path)
        self._exit_manager()
        self._update_selection_label()

    def _exit_manager(self, *args):
        self.file_manager.close()

    def _update_selection_label(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        if not self.selected:
            self.ids.selection_label.text = app.tr("no_selection")
        else:
            names = "\n".join("• " + os.path.basename(p) for p in self.selected)
            self.ids.selection_label.text = names

    # ------- الإرسال -------
    def send(self):
        app = MDApp.get_running_app()
        host = self.ids.host_field.text.strip()
        port = self.ids.port_field.text.strip() or "2121"
        if not host:
            app.toast(app.tr("enter_ip"))
            return
        if not self.selected:
            app.toast(app.tr("no_selection"))
            return

        app.toast(app.tr("sending"))
        files = list(self.selected)
        threading.Thread(
            target=self._do_upload, args=(host, port, files), daemon=True
        ).start()

    def _do_upload(self, host, port, files):
        app = MDApp.get_running_app()
        try:
            success, errors = upload_files(host, port, files)
            if errors and success == 0:
                Clock.schedule_once(lambda dt: app.toast(app.tr("send_failed")))
            else:
                Clock.schedule_once(lambda dt: self._on_sent())
        except Exception:
            Clock.schedule_once(lambda dt: app.toast(app.tr("connect_failed")))

    def _on_sent(self):
        app = MDApp.get_running_app()
        app.toast(app.tr("send_success"))
        self.selected = []
        self._update_selection_label()
