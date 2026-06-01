# -*- coding: utf-8 -*-
"""
عميل FTP
FTP client used by the Send tab. Connects to another device's FTP server
(running this same app) and uploads the selected files using the built-in
ftplib module.
"""
import os
from ftplib import FTP


def upload_files(host, port, file_paths, progress_cb=None):
    """
    رفع قائمة ملفات إلى خادم FTP بعيد.

    host: عنوان IP للجهاز المستقبل
    port: المنفذ
    file_paths: قائمة بمسارات الملفات المراد إرسالها
    progress_cb: دالة اختيارية تُستدعى (index, total, filename) لكل ملف

    تُرجع (success_count, errors) حيث errors قائمة برسائل الأخطاء.
    """
    errors = []
    success = 0
    total = len(file_paths)

    ftp = FTP()
    ftp.connect(host=host, port=int(port), timeout=15)
    ftp.login()  # دخول مجهول anonymous
    try:
        for i, path in enumerate(file_paths):
            name = os.path.basename(path)
            if progress_cb:
                progress_cb(i + 1, total, name)
            try:
                with open(path, "rb") as f:
                    ftp.storbinary("STOR " + name, f)
                success += 1
            except Exception as e:
                errors.append(name + ": " + str(e))
    finally:
        try:
            ftp.quit()
        except Exception:
            try:
                ftp.close()
            except Exception:
                pass

    return success, errors
