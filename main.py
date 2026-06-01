# -*- coding: utf-8 -*-
"""
File Sharing App over FTP through a phone Hotspot.
Built entirely in Python using Kivy 2.2.0 and KivyMD 1.1.1.
"""

import arabic_reshaper
from bidi.algorithm import get_display
import os

from kivy.utils import platform
if platform == "android":
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.INTERNET,
            Permission.ACCESS_NETWORK_STATE,
            Permission.ACCESS_WIFI_STATE,
        ])
    except Exception as e:
        print(f"Permission request error: {e}")

from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivymd.app import MDApp

from app.localization import translate
from app.settings_store import SettingsStore
from app.ftp_server import FtpServerManager

# Register tabs
from app.screens.home_tab import HomeTab          # noqa: F401
from app.screens.send_tab import SendTab          # noqa: F401
from app.screens.receive_tab import ReceiveTab    # noqa: F401
from app.screens.settings_tab import SettingsTab  # noqa: F401

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KV_DIR = os.path.join(BASE_DIR, "kv")
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")

def ar(text):
    return get_display(arabic_reshaper.reshape(text))

def _register_arabic_font():
    regular = os.path.join(FONT_DIR, "Cairo-Regular.ttf")
    bold = os.path.join(FONT_DIR, "Cairo-Bold.ttf")
    if os.path.exists(regular):
        try:
            LabelBase.register(
                name="Cairo",
                fn_regular=regular,
                fn_bold=bold if os.path.exists(bold) else regular,
            )
        except Exception as e:
            print(f"Font registration error: {e}")

class FileShareApp(MDApp):
    def build(self):
        self.title = ar("File Share")
        _register_arabic_font()

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"

        config_path = os.path.join(self.user_data_dir, "config.json")
        self.settings = SettingsStore(config_path)
        self.lang = self.settings.get("language")
        if self.settings.get("dark_mode"):
            self.theme_cls.theme_style = "Dark"

        shared_dir = self._shared_dir()
        self.server = FtpServerManager(shared_dir, port=int(self.settings.get("port")))

        for kv in ("home.kv", "send.kv", "receive.kv", "settings.kv"):
            Builder.load_file(os.path.join(KV_DIR, kv))

        self.root_widget = Builder.load_file(os.path.join(KV_DIR, "main.kv"))
        return self.root_widget

    def on_start(self):
        self.refresh_ui()

    def _shared_dir(self):
        if platform == "android":
            try:
                from android.storage import primary_external_storage_path
                base = primary_external_storage_path()
                path = os.path.join(base, "FileShare")
            except Exception as e:
                print(f"Android storage error: {e}")
                path = os.path.join(self.user_data_dir, "FileShare")
        else:
            path = os.path.join(os.path.expanduser("~"), "FileShare")
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            print(f"Directory creation error: {e}")
            path = os.path.join(self.user_data_dir, "FileShare")
            os.makedirs(path, exist_ok=True)
        return path

    def tr(self, key):
        return translate(key, self.lang)

    def set_language(self, lang):
        if lang not in ("ar", "en"):
            return
        self.lang = lang
        self.settings.set("language", lang)
        self.refresh_ui()

    def refresh_ui(self):
        ids = self.root_widget.ids
        # Arabic reshaping for top bar
        ids.top_bar.title = ar(self.tr("app_title"))
        ids.top_bar.font_name = "Cairo"

        ids.nav_home.text = self.tr("tab_home")
        ids.nav_send.text = self.tr("tab_send")
        ids.nav_receive.text = self.tr("tab_receive")
        ids.nav_settings.text = self.tr("tab_settings")

        for tab_id in ("home_tab", "send_tab", "receive_tab", "settings_tab"):
            tab = ids.get(tab_id)
            if tab is not None and hasattr(tab, "refresh_text"):
                tab.refresh_text()

    def set_dark_mode(self, value):
        self.theme_cls.theme_style = "Dark" if value else "Light"
        self.settings.set("dark_mode", bool(value))

    def start_server(self):
        self.server.port = int(self.settings.get("port"))
        self.server.start()

    def toast(self, message):
        try:
            from kivymd.toast import toast
            toast(message)
        except Exception:
            print(message)

    def on_stop(self):
        try:
            self.server.stop()
        except Exception:
            pass

if __name__ == "__main__":
    FileShareApp().run()