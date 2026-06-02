# -*- coding: utf-8 -*-
"""
File Sharing App over FTP through a phone Hotspot.
Built entirely in Python using Kivy 2.2.0 and KivyMD 1.1.1.
Redesigned UI: dark theme, teal accent, custom bottom navigation.
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
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivymd.app import MDApp

from app.localization import translate
from app.settings_store import SettingsStore
from app.ftp_server import FtpServerManager

# Register screens and widgets
from app.screens.home_tab import HomeTab          # noqa: F401
from app.screens.send_tab import SendTab          # noqa: F401
from app.screens.receive_tab import ReceiveTab    # noqa: F401
from app.screens.settings_tab import SettingsTab  # noqa: F401
from app.widgets.nav_item import NavItem          # noqa: F401

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
    # Palette constants exposed for kv if needed
    C_BG      = get_color_from_hex("#0f1117")
    C_SURFACE = get_color_from_hex("#1a1d27")
    C_ACCENT  = get_color_from_hex("#00d4aa")
    C_TEXT    = get_color_from_hex("#e8eaf6")

    def build(self):
        self.title = ar("File Share")
        _register_arabic_font()

        # Force dark theme; our colours are hard-coded in kv
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        config_path = os.path.join(self.user_data_dir, "config.json")
        self.settings = SettingsStore(config_path)
        self.lang = self.settings.get("language")

        shared_dir = self._shared_dir()
        self.server = FtpServerManager(
            shared_dir, port=int(self.settings.get("port"))
        )

        for kv in ("home.kv", "send.kv", "receive.kv", "settings.kv"):
            Builder.load_file(os.path.join(KV_DIR, kv))

        root = Builder.load_file(os.path.join(KV_DIR, "main.kv"))
        return root

    def on_start(self):
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.refresh_ui(), 0)

    # ── helpers ──────────────────────────────────────────────

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

    # ── navigation ───────────────────────────────────────────

    def switch_tab(self, tab_name):
        """Switch the ScreenManager and update nav highlight."""
        sm = self.root.ids.screen_manager
        sm.current = tab_name

        nav_ids = {
            "server":   "nav_server",
            "send":     "nav_send",
            "receive":  "nav_receive",
            "settings": "nav_settings",
        }
        for name, wid_id in nav_ids.items():
            wid = self.root.ids.get(wid_id)
            if wid:
                wid.active = (name == tab_name)

        # Update server dot
        dot = self.root.ids.get("server_dot")
        if dot:
            dot.text_color = (
                get_color_from_hex("#00e676")
                if self.server.is_running
                else get_color_from_hex("#4a5278")
            )

    # ── UI refresh ───────────────────────────────────────────

    def set_language(self, lang):
        if lang not in ("ar", "en"):
            return
        self.lang = lang
        self.settings.set("language", lang)
        self.refresh_ui()

    def refresh_ui(self):
        if not self.root:
            return
        ids = self.root.ids
        ids.top_title.text = self.tr("app_title")
        ids.nav_server.nav_text  = self.tr("tab_home")
        ids.nav_send.nav_text    = self.tr("tab_send")
        ids.nav_receive.nav_text = self.tr("tab_receive")
        ids.nav_settings.nav_text= self.tr("tab_settings")

        for tab_id in ("home_tab", "send_tab", "receive_tab", "settings_tab"):
            tab = ids.get(tab_id)
            if tab is not None and hasattr(tab, "refresh_text"):
                tab.refresh_text()

    def set_dark_mode(self, value):
        # Our UI is always dark; this just persists the pref
        self.settings.set("dark_mode", bool(value))

    def start_server(self):
        self.server.port = int(self.settings.get("port"))
        self.server.start()
        # Update dot
        dot = self.root.ids.get("server_dot")
        if dot:
            dot.text_color = get_color_from_hex("#00e676")

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
