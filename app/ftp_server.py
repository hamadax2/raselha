# -*- coding: utf-8 -*-
"""
خادم FTP
FTP server wrapper built on pyftpdlib. Runs in a background thread so it does
not block the Kivy UI. Allows anonymous read/write access to one shared folder
so other devices on the same Hotspot can upload and download files.
"""
import os
import threading

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class FtpServerManager:
    def __init__(self, shared_dir, port=2121):
        self.shared_dir = shared_dir
        self.port = port
        self._server = None
        self._thread = None
        self._running = False
        os.makedirs(self.shared_dir, exist_ok=True)

    @property
    def is_running(self):
        return self._running

    def start(self):
        """تشغيل الخادم في خيط منفصل."""
        if self._running:
            return

        os.makedirs(self.shared_dir, exist_ok=True)

        authorizer = DummyAuthorizer()
        # وصول مجهول (anonymous) مع كامل الصلاحيات على مجلد المشاركة
        # e=change dir, l=list, r=read, a=append, d=delete, f=rename,
        # m=mkdir, w=store(upload), M=chmod, T=set timestamp
        authorizer.add_anonymous(self.shared_dir, perm="elradfmwMT")

        handler = FTPHandler
        handler.authorizer = authorizer
        handler.banner = "File Share FTP server ready."
        # نطاق المنافذ السلبية (passive) لتفادي مشاكل بعض الشبكات
        handler.passive_ports = range(60000, 60010)

        self._server = FTPServer(("0.0.0.0", self.port), handler)
        self._server.max_cons = 64
        self._server.max_cons_per_ip = 16

        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._running = True
        self._thread.start()

    def _serve(self):
        try:
            self._server.serve_forever()
        except Exception:
            pass
        finally:
            self._running = False

    def stop(self):
        """إيقاف الخادم."""
        if not self._running:
            return
        try:
            if self._server is not None:
                self._server.close_all()
        except Exception:
            pass
        self._running = False
        self._server = None

    def list_files(self):
        """إرجاع قائمة بأسماء الملفات الموجودة في مجلد المشاركة."""
        try:
            return sorted(
                f for f in os.listdir(self.shared_dir)
                if os.path.isfile(os.path.join(self.shared_dir, f))
            )
        except Exception:
            return []

    def delete_file(self, name):
        try:
            os.remove(os.path.join(self.shared_dir, name))
            return True
        except Exception:
            return False
