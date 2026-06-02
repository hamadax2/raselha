# -*- coding: utf-8 -*-
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

ACCENT     = get_color_from_hex("#00d4aa")
ACCENT_DIM = get_color_from_hex("#00d4aa22")
SURFACE    = get_color_from_hex("#22263a")
TEXT_MID   = get_color_from_hex("#8892b0")


class SettingsTab(MDBoxLayout):

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self._init(), 0)

    def _init(self):
        app = MDApp.get_running_app()
        self.ids.dark_switch.active = bool(app.settings.get("dark_mode"))
        self.ids.port_field.text    = str(app.settings.get("port"))
        self.refresh_text()

    def refresh_text(self):
        app = MDApp.get_running_app()
        if not self.ids: return
        self.ids.language_label.text   = app.tr("language").upper()
        self.ids.btn_en.text           = app.tr("english")
        self.ids.btn_ar.text           = app.tr("arabic")
        self.ids.appearance_label.text = app.tr("appearance").upper()
        self.ids.dark_label.text       = app.tr("dark_mode")
        self.ids.network_label.text    = app.tr("network").upper()
        self.ids.port_field.hint_text  = app.tr("server_port")
        self.ids.about_label.text      = app.tr("about").upper()
        self.ids.about_value.text      = app.tr("about_text")
        self._sync_lang_buttons()

    def _sync_lang_buttons(self):
        app = MDApp.get_running_app()
        is_en = app.lang == "en"
        self.ids.btn_en.md_bg_color = ACCENT_DIM if is_en  else SURFACE
        self.ids.btn_en.text_color  = ACCENT      if is_en  else TEXT_MID
        self.ids.btn_ar.md_bg_color = ACCENT_DIM if not is_en else SURFACE
        self.ids.btn_ar.text_color  = ACCENT      if not is_en else TEXT_MID

    def set_language(self, lang):
        MDApp.get_running_app().set_language(lang)
        self._sync_lang_buttons()

    def toggle_dark(self, value):
        MDApp.get_running_app().set_dark_mode(value)

    def on_port(self, value):
        text = (value or "").strip()
        if text.isdigit():
            MDApp.get_running_app().settings.set("port", int(text))
