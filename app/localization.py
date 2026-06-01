# -*- coding: utf-8 -*-
"""
نظام الترجمة (عربي / إنجليزي)
Localization system (Arabic / English)

- يحتوي على كل النصوص المستخدمة في الواجهة.
- يقوم بإعادة تشكيل الحروف العربية لعرضها بشكل صحيح في Kivy
  باستخدام arabic_reshaper و python-bidi.
"""

# محاولة استيراد مكتبات تشكيل العربية (اختيارية لكنها مهمة لعرض العربية)
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    _ARABIC_SUPPORT = True
except Exception:  # pragma: no cover
    _ARABIC_SUPPORT = False


# اللغات المدعومة
LANGUAGES = ("ar", "en")

# كل النصوص: key -> {"ar": "...", "en": "..."}
STRINGS = {
    "app_title": {"ar": "مشاركة الملفات", "en": "File Share"},

    # التبويبات
    "tab_home": {"ar": "الخادم", "en": "Server"},
    "tab_send": {"ar": "إرسال", "en": "Send"},
    "tab_receive": {"ar": "الملفات", "en": "Files"},
    "tab_settings": {"ar": "الإعدادات", "en": "Settings"},

    # الشاشة الرئيسية / الخادم
    "server_status": {"ar": "حالة الخادم", "en": "Server Status"},
    "server_running": {"ar": "الخادم يعمل", "en": "Server Running"},
    "server_stopped": {"ar": "الخادم متوقف", "en": "Server Stopped"},
    "start_server": {"ar": "تشغيل الخادم", "en": "Start Server"},
    "stop_server": {"ar": "إيقاف الخادم", "en": "Stop Server"},
    "your_ip": {"ar": "عنوان جهازك", "en": "Your IP Address"},
    "port": {"ar": "المنفذ", "en": "Port"},
    "home_hint": {
        "ar": "شغّل نقطة اتصال الهاتف (Hotspot)، ثم شغّل الخادم. "
              "اطلب من الطرف الآخر فتح تبويب الإرسال وإدخال العنوان والمنفذ أعلاه.",
        "en": "Turn on your phone Hotspot, then start the server. "
              "Ask the other device to open the Send tab and enter the IP and port shown above.",
    },

    # شاشة الإرسال
    "connect_title": {"ar": "الاتصال بجهاز آخر", "en": "Connect To A Device"},
    "host_ip": {"ar": "عنوان الجهاز المستقبل", "en": "Receiver IP Address"},
    "host_port": {"ar": "المنفذ", "en": "Port"},
    "pick_files": {"ar": "اختيار ملفات", "en": "Pick Files"},
    "send_files": {"ar": "إرسال الملفات", "en": "Send Files"},
    "selected_files": {"ar": "الملفات المختارة", "en": "Selected Files"},
    "no_selection": {"ar": "لم يتم اختيار ملفات بعد", "en": "No files selected yet"},
    "sending": {"ar": "جاري الإرسال...", "en": "Sending..."},
    "send_success": {"ar": "تم إرسال الملفات بنجاح", "en": "Files sent successfully"},
    "send_failed": {"ar": "فشل الإرسال", "en": "Send failed"},
    "connect_failed": {"ar": "تعذّر الاتصال بالجهاز", "en": "Could not connect to device"},
    "enter_ip": {"ar": "الرجاء إدخال عنوان الجهاز", "en": "Please enter the device IP"},

    # شاشة الملفات المستلمة
    "shared_files": {"ar": "الملفات المستلمة", "en": "Received Files"},
    "refresh": {"ar": "تحديث", "en": "Refresh"},
    "no_files": {"ar": "لا توجد ملفات", "en": "No files yet"},
    "delete": {"ar": "حذف", "en": "Delete"},
    "deleted": {"ar": "تم الحذف", "en": "Deleted"},
    "folder_label": {"ar": "مجلد المشاركة", "en": "Shared Folder"},

    # الإعدادات
    "settings_title": {"ar": "الإعدادات", "en": "Settings"},
    "language": {"ar": "اللغة", "en": "Language"},
    "arabic": {"ar": "العربية", "en": "Arabic"},
    "english": {"ar": "الإنجليزية", "en": "English"},
    "appearance": {"ar": "المظهر", "en": "Appearance"},
    "dark_mode": {"ar": "الوضع الداكن", "en": "Dark Mode"},
    "network": {"ar": "الشبكة", "en": "Network"},
    "server_port": {"ar": "منفذ الخادم", "en": "Server Port"},
    "about": {"ar": "حول التطبيق", "en": "About"},
    "about_text": {
        "ar": "تطبيق لمشاركة الملفات (صور، فيديو، صوتيات وأي نوع) عبر بروتوكول FTP "
              "من خلال شبكة نقطة الاتصال (Hotspot). مبني بالكامل بلغة بايثون باستخدام Kivy و KivyMD.",
        "en": "An app to share files (photos, video, audio and any type) over FTP "
              "through a phone Hotspot network. Built entirely in Python with Kivy and KivyMD.",
    },

    # عام
    "ok": {"ar": "حسناً", "en": "OK"},
    "cancel": {"ar": "إلغاء", "en": "Cancel"},
    "close": {"ar": "إغلاق", "en": "Close"},
    "copied": {"ar": "تم النسخ", "en": "Copied"},
}


def shape(text, lang):
    """إعادة تشكيل النص العربي ليُعرض بشكل صحيح في Kivy."""
    if lang == "ar" and _ARABIC_SUPPORT and any("\u0600" <= c <= "\u06FF" for c in text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text


def translate(key, lang="ar"):
    """إرجاع النص المترجم والمشكّل للمفتاح المعطى."""
    entry = STRINGS.get(key)
    if entry is None:
        return key
    raw = entry.get(lang, entry.get("en", key))
    return shape(raw, lang)
