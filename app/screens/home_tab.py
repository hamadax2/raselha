# -*- coding: utf-8 -*-
"""
تبويب الخادم (الرئيسية)
Home / Server tab: start & stop the FTP server and show the device IP and port.
"""
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from app.network_utils import get_local_ip


class HomeTab(MDBoxLayout):
    """واجهة تبويب الخادم. القواعد معرفة في kv/home.kv"""

    def on_kv_post(self, base_widget):
        # تحديث المعلومات عند بناء الواجهة
        self.refresh_status()
        self.refresh_text()

    # ------- النصوص (للترجمة) -------
    def refresh_text(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        self.ids.section_status.text = app.tr("server_status")
        self.ids.ip_label.text = app.tr("your_ip")
        self.ids.port_label.text = app.tr("port")
        self.ids.hint_label.text = app.tr("home_hint")
        self.refresh_status()

    # ------- الحالة -------
    def refresh_status(self):
        app = MDApp.get_running_app()
        if not self.ids:
            return
        # Check if server is initialized
        if not app.server:
            self.ids.status_value.text = app.tr("server_stopped")
            self.ids.status_value.theme_text_color = "Custom"
            self.ids.status_value.text_color = (0.83, 0.18, 0.18, 1)
            self.ids.toggle_btn.text = app.tr("start_server")
            self.ids.ip_value.text = get_local_ip()
            self.ids.port_value.text = str(app.settings.get("port"))
            return
            
        running = app.server.is_running
        self.ids.status_value.text = app.tr(
            "server_running" if running else "server_stopped"
        )
        self.ids.status_value.theme_text_color = "Custom"
        self.ids.status_value.text_color = (
            (0.16, 0.65, 0.27, 1) if running else (0.83, 0.18, 0.18, 1)
        )
        self.ids.toggle_btn.text = app.tr("stop_server" if running else "start_server")
        self.ids.ip_value.text = get_local_ip()
        self.ids.port_value.text = str(app.settings.get("port"))

    # ------- الأحداث -------
    def toggle_server(self):
        app = MDApp.get_running_app()
        if not app.server:
            return
        if app.server.is_running:
            app.server.stop()
        else:
            app.start_server()
        self.refresh_status()
