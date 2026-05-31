# -*- coding: utf-8 -*-
"""
أدوات الشبكة
Network helpers: discover the local IP address of the device.
"""
import socket


def get_local_ip():
    """
    إرجاع عنوان IP المحلي للجهاز على شبكة نقطة الاتصال (Hotspot).
    لا يقوم بإرسال أي بيانات فعلية، فقط يفتح socket لمعرفة العنوان المحلي.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # عنوان خارجي وهمي فقط لتحديد الواجهة الصحيحة
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip
