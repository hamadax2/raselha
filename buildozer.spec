[app]

# اسم التطبيق - App name
title = File Share

# اسم الحزمة - Package name
package.name = fileshare
package.domain = org.fileshare

# المصادر - Source code
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,otf,atlas
source.include_patterns = kv/*,app/*,assets/*

# الإصدار - Version
version = 1.0

# المتطلبات - Requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyftpdlib,arabic_reshaper,python-bidi,plyer

# التوجيه - Orientation
orientation = portrait

# شاشة كاملة - Fullscreen
fullscreen = 0

# الصلاحيات المطلوبة - Android permissions
# الإنترنت والوصول لحالة الشبكة ضروريان لخادم FTP عبر الـ Hotspot
# وصلاحيات التخزين لقراءة وكتابة الملفات المشتركة
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# واجهة برمجة تطبيقات أندرويد - Android API
android.api = 34
android.minapi = 24
android.ndk_api = 24

# البنى المعمارية - Architectures
android.archs = arm64-v8a

# قبول تراخيص الـ SDK تلقائياً
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1

