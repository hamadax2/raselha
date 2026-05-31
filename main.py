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
import sys

# Set environment variables before any kivy imports
os.environ.setdefault('KIVY_LOG_LEVEL', 'warning')

from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder

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
    if os.path.exists(regular):
        try:
            LabelBase.register(
                name="Roboto",
                fn_regular=regular,
                fn_bold=regular,  # Use regular as bold since bold is not available
            )
        except Exception as e:
            pass
    

class FileShareApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server = None
        self._permissions_granted = False
    
    def build(self):
        self.title = "File Share"

        # الخطوط (لدعم العربية)
        _register_arabic_font()

        # المظهر
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.material_style = "M3"

        # الإعدادات المحفوظة (use app data dir which doesn't need permissions)
        config_path = os.path.join(self.user_data_dir, "config.json")
        self.settings = SettingsStore(config_path)
        self.lang = self.settings.get("language")
        if self.settings.get("dark_mode"):
            self.theme_cls.theme_style = "Dark"

        # تحميل قواعد التبويبات المنفصلة أولاً
        for kv in ("home.kv", "send.kv", "receive.kv", "settings.kv"):
            Builder.load_file(os.path.join(KV_DIR, kv))

        # ثم تحميل الواجهة الرئيسية وإرجاعها كجذر للتطبيق
        self.root_widget = Builder.load_file(os.path.join(KV_DIR, "main.kv"))
        return self.root_widget

    def on_start(self):
        # Request permissions on Android after UI is built
        if platform == "android":
            self._request_android_permissions()
        else:
            self._init_after_permissions()

    def _request_android_permissions(self):
        """Request Android permissions with callback."""
        try:
            from android.permissions import request_permissions, Permission
            
            def callback(permissions, results):
                # Check if all permissions were granted
                if all(results):
                    self._permissions_granted = True
                else:
                    self._permissions_granted = False
                # Initialize app after permissions dialog is done
                Clock.schedule_once(lambda dt: self._init_after_permissions(), 0.5)
            
            request_permissions([
                Permission.INTERNET,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.ACCESS_NETWORK_STATE,
                Permission.ACCESS_WIFI_STATE,
            ], callback)
        except Exception as e:
            # If permission request fails, try to continue anyway
            Clock.schedule_once(lambda dt: self._init_after_permissions(), 0.5)

    def _init_after_permissions(self):
        """Initialize storage and server after permissions are handled."""
        try:
            # مجلد المشاركة الذي يستقبل الملفات
            shared_dir = self._shared_dir()
            self.server = FtpServerManager(shared_dir, port=int(self.settings.get("port")))
            self.refresh_ui()
        except Exception as e:
            # Fallback to app data directory
            shared_dir = os.path.join(self.user_data_dir, "FileShare")
            os.makedirs(shared_dir, exist_ok=True)
            self.server = FtpServerManager(shared_dir, port=int(self.settings.get("port")))
            self.refresh_ui()

    # ------- المجلدات -------
    def _shared_dir(self):
        if platform == "android":
            try:
                from android.storage import primary_external_storage_path
                base = primary_external_storage_path()
                if base:
                    path = os.path.join(base, "FileShare")
                    os.makedirs(path, exist_ok=True)
                    return path
            except Exception as e:
                pass
        
        # Fallback for non-Android or if external storage fails
        if platform == "android":
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
        if not self.root_widget:
            return
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
        if self.server:
            self.server.port = int(self.settings.get("port"))
            self.server.start()

    # ------- رسائل سريعة -------
    def toast(self, message):
        try:
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text=message).open()
        except Exception:
            pass

    def on_stop(self):
        try:
            if self.server:
                self.server.stop()
        except Exception:
            pass


if __name__ == "__main__":
    FileShareApp().run()
