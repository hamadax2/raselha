# -*- coding: utf-8 -*-
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from app.network_utils import get_local_ip

ACCENT = get_color_from_hex("#00d4aa")
DANGER = get_color_from_hex("#ff4d6d")


class HomeTab(MDBoxLayout):

    def on_kv_post(self, base_widget):
        # Defer until app.root is fully assigned
        Clock.schedule_once(lambda dt: self._init(), 0)

    def _init(self):
        self.refresh_text()
        self.refresh_status()

    def refresh_text(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        self.ids.section_status.text = app.tr("server_status").upper()
        self.ids.ip_label.text       = "NETWORK INFO"
        self.ids.hint_label.text     = app.tr("home_hint")

    def refresh_status(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        running = app.server.is_running

        self.ids.status_value.text       = app.tr("server_running" if running else "server_stopped")
        self.ids.status_value.text_color = ACCENT if running else DANGER
        self.ids.status_icon.text_color  = ACCENT if running else DANGER
        self.ids.toggle_btn.text         = app.tr("stop_server" if running else "start_server")
        self.ids.toggle_btn.md_bg_color  = DANGER if running else ACCENT
        self.ids.toggle_btn.text_color   = (
            get_color_from_hex("#e8eaf6") if running else get_color_from_hex("#0a0f1e")
        )
        self.ids.ip_value.text   = get_local_ip() if running else "—"
        self.ids.port_value.text = str(app.settings.get("port"))

        # Safe root access
        root = app.root
        if root:
            dot = root.ids.get("server_dot")
            if dot:
                dot.text_color = ACCENT if running else get_color_from_hex("#4a5278")

    def toggle_server(self):
        app = MDApp.get_running_app()
        if app.server.is_running:
            app.server.stop()
            app.toast(app.tr("server_stopped"))
        else:
            app.start_server()
            app.toast(app.tr("server_running"))
        self.refresh_status()
