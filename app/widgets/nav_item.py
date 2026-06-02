# -*- coding: utf-8 -*-
"""
Custom bottom navigation item.
Avoids MDCard entirely — uses MDBoxLayout + radius for rounded bg.
"""
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_string("""
#:import get_color_from_hex kivy.utils.get_color_from_hex

<NavItem>:
    orientation: "vertical"
    spacing: "2dp"
    padding: ["4dp", "0dp", "4dp", "0dp"]
    size_hint_x: 1

    # Indicator stripe
    MDBoxLayout:
        size_hint_y: None
        height: "3dp"
        md_bg_color: get_color_from_hex("#00d4aa") if root.active else (0, 0, 0, 0)
        radius: [0, 0, 3, 3]

    MDIcon:
        id: _icon
        icon: root.nav_icon
        halign: "center"
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#00d4aa") if root.active else get_color_from_hex("#4a5278")
        font_size: "22sp"
        size_hint_y: None
        height: "26dp"

    MDLabel:
        id: _label
        text: root.nav_text
        halign: "center"
        font_name: "Cairo"
        font_style: "Caption"
        bold: True
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#00d4aa") if root.active else get_color_from_hex("#4a5278")
        size_hint_y: None
        height: "16dp"
""")


class NavItem(MDBoxLayout):
    nav_icon = StringProperty("circle")
    nav_text = StringProperty("")
    tab_name = StringProperty("")
    active   = BooleanProperty(False)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            from kivymd.app import MDApp
            MDApp.get_running_app().switch_tab(self.tab_name)
            return True
        return super().on_touch_up(touch)
