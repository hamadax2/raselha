# -*- coding: utf-8 -*-
"""
تطبيق مشاركة الملفات عبر FTP من خلال نقطة اتصال الهاتف (Hotspot)
File Sharing App over FTP through a phone Hotspot.

مبني بالكامل بلغة بايثون باستخدام Kivy و KivyMD فقط.
Built entirely in Python using Kivy and KivyMD only.

نقطة الدخول: تقوم بتحميل ملفات .kv المنفصلة، وضبط الخطوط واللغة،
وإدارة خادم FTP والتبديل بين العربية والإنجليزية.
"""
import os

from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.utils import platform

from kivymd.app import MDApp

from app.localization import translate
from app.settings_store import SettingsStore
from app.ftp_server import FtpServerManager

# تسجيل كلاسات التبويبات حتى تتعرف عليها ملفات kv
from app.screens.home_tab import HomeTab          # noqa: F401
from app.screens.send_tab import SendTab          # noqa: F401
from app.screens.receive_tab import ReceiveTab    # noqa: F401
from app.screens.settings_tab import SettingsTab  # noqa: F401


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KV_DIR = os.path.join(BASE_DIR, "kv")
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")


def _register_arabic_font():
    """
    تسجيل خط يدعم العربية بديلاً عن الخط الافتراضي (Roboto) في KivyMD
    حتى تُعرض الحروف العربية في كل أنحاء التطبيق.
    ضع ملفات الخط داخل assets/fonts/ (مثل خط Cairo).
    """
    regular = os.path.join(FONT_DIR, "Cairo-Regular.ttf")
    bold = os.path.join(FONT_DIR, "Cairo-Bold.ttf")
    if os.path.exists(regular):
        LabelBase.register(
            name="Roboto",
            fn_regular=regular,
            fn_bold=bold if os.path.exists(bold) else regular,
        )


class FileShareApp(MDApp):
    def build(self):
        self.title = "File Share"

        # الخطوط (لدعم العربية)
        _register_arabic_font()

        # المظهر
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.material_style = "M3"

        # الإعدادات المحفوظة
        config_path = os.path.join(self.user_data_dir, "config.json")
        self.settings = SettingsStore(config_path)
        self.lang = self.settings.get("language")
        if self.settings.get("dark_mode"):
            self.theme_cls.theme_style = "Dark"

        # مجلد المشاركة الذي يستقبل الملفات
        shared_dir = self._shared_dir()
        self.server = FtpServerManager(shared_dir, port=int(self.settings.get("port")))

        # تحميل قواعد التبويبات المنفصلة أولاً
        for kv in ("home.kv", "send.kv", "receive.kv", "settings.kv"):
            Builder.load_file(os.path.join(KV_DIR, kv))

        # ثم تحميل الواجهة الرئيسية وإرجاعها كجذر للتطبيق
        self.root_widget = Builder.load_file(os.path.join(KV_DIR, "main.kv"))
        return self.root_widget

    def on_start(self):
        self.refresh_ui()

    # ------- المجلدات -------
    def _shared_dir(self):
        if platform == "android":
            try:
                from android.storage import primary_external_storage_path  # type: ignore
                base = primary_external_storage_path()
                path = os.path.join(base, "FileShare")
            except Exception:
                path = os.path.join(self.user_data_dir, "FileShare")
        else:
            path = os.path.join(os.path.expanduser("~"), "FileShare")
        os.makedirs(path, exist_ok=True)
        return path

    # ------- الترجمة -------
    def tr(self, key):
        return translate(key, self.lang)

    def set_language(self, lang):
        if lang not in ("ar", "en"):
            return
        self.lang = lang
        self.settings.set("language", lang)
        self.refresh_ui()

    def refresh_ui(self):
        """تحديث كل النصوص في الواجهة بعد تغيير اللغة."""
        ids = self.root_widget.ids
        ids.top_bar.title = self.tr("app_title")
        ids.nav_home.text = self.tr("tab_home")
        ids.nav_send.text = self.tr("tab_send")
        ids.nav_receive.text = self.tr("tab_receive")
        ids.nav_settings.text = self.tr("tab_settings")

        for tab_id in ("home_tab", "send_tab", "receive_tab", "settings_tab"):
            tab = ids.get(tab_id)
            if tab is not None and hasattr(tab, "refresh_text"):
                tab.refresh_text()

    # ------- المظهر -------
    def set_dark_mode(self, value):
        self.theme_cls.theme_style = "Dark" if value else "Light"
        self.settings.set("dark_mode", bool(value))

    # ------- الخادم -------
    def start_server(self):
        self.server.port = int(self.settings.get("port"))
        self.server.start()

    # ------- رسائل سريعة -------
    def toast(self, message):
        try:
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text=message).open()
        except Exception:
            print(message)

    def on_stop(self):
        try:
            self.server.stop()
        except Exception:
            pass


if __name__ == "__main__":
    FileShareApp().run()
