# -*- coding: utf-8 -*-
"""
تخزين الإعدادات
Persist user settings (language, theme, port) to a JSON file.
"""
import json
import os


DEFAULTS = {
    "language": "ar",     # اللغة الافتراضية: العربية
    "dark_mode": False,
    "port": 2121,
}


class SettingsStore:
    def __init__(self, path):
        self.path = path
        self.data = dict(DEFAULTS)
        self.load()

    def load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.data.update({k: saved[k] for k in saved if k in DEFAULTS})
        except Exception:
            # في حال تلف الملف نرجع للقيم الافتراضية
            self.data = dict(DEFAULTS)

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get(self, key):
        return self.data.get(key, DEFAULTS.get(key))

    def set(self, key, value):
        self.data[key] = value
        self.save()
