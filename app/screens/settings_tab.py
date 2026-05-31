# -*- coding: utf-8 -*-
"""
تبويب الإعدادات
Settings tab: switch language (Arabic / English), toggle dark mode and change
the FTP server port.
"""
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout


class SettingsTab(MDBoxLayout):
    """واجهة تبويب الإعدادات. القواعد معرفة في kv/settings.kv"""

    def on_kv_post(self, base_widget):
        self.refresh_text()
        app = MDApp.get_running_app()
        # ضبط القيم الحالية
        self.ids.dark_switch.active = bool(app.settings.get("dark_mode"))
        self.ids.port_field.text = str(app.settings.get("port"))
        self._sync_lang_buttons()

    def refresh_text(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        self.ids.settings_title.text = app.tr("settings_title")
        self.ids.language_label.text = app.tr("language")
        self.ids.btn_ar.text = app.tr("arabic")
        self.ids.btn_en.text = app.tr("english")
        self.ids.appearance_label.text = app.tr("appearance")
        self.ids.dark_label.text = app.tr("dark_mode")
        self.ids.network_label.text = app.tr("network")
        self.ids.port_field.hint_text = app.tr("server_port")
        self.ids.about_label.text = app.tr("about")
        self.ids.about_value.text = app.tr("about_text")
        self._sync_lang_buttons()

    def _sync_lang_buttons(self):
        app = MDApp.get_running_app()
        is_ar = app.lang == "ar"
        # تمييز اللغة المختارة
        self.ids.btn_ar.md_bg_color = (
            app.theme_cls.primary_color if is_ar else (0, 0, 0, 0)
        )
        self.ids.btn_en.md_bg_color = (
            app.theme_cls.primary_color if not is_ar else (0, 0, 0, 0)
        )

    # ------- الأحداث -------
    def set_language(self, lang):
        app = MDApp.get_running_app()
        app.set_language(lang)
        self._sync_lang_buttons()

    def toggle_dark(self, value):
        app = MDApp.get_running_app()
        app.set_dark_mode(value)

    def on_port(self, value):
        app = MDApp.get_running_app()
        text = (value or "").strip()
        if text.isdigit():
            app.settings.set("port", int(text))
