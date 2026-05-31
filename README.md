# مشاركة الملفات عبر FTP | File Share over FTP

تطبيق لمشاركة الملفات (صور، فيديو، صوتيات، وأي نوع من الملفات) بين الأجهزة
عبر بروتوكول **FTP** من خلال شبكة **نقطة اتصال الهاتف (Hotspot)**.
مبني بالكامل بلغة **بايثون** باستخدام **Kivy** و **KivyMD** فقط — لا توجد أي لغة أخرى.

An app to share files (photos, video, audio, and any file type) between devices
over **FTP** through a phone **Hotspot** network. Built entirely in **Python**
using **Kivy** and **KivyMD** only — no other languages.

---

## المميزات | Features

- خادم FTP مدمج لاستقبال الملفات | Built-in FTP server to receive files
- إرسال عدة ملفات إلى جهاز آخر | Send multiple files to another device
- استعراض وحذف الملفات المستلمة | Browse and delete received files
- واجهة عربية بالكامل مع إمكانية التبديل للإنجليزية | Full Arabic UI with English toggle
- الوضع الداكن وحفظ الإعدادات | Dark mode and persistent settings

## بنية المشروع | Project structure

```
main.py                  # نقطة الدخول | entry point
requirements.txt
buildozer.spec           # إعداد بناء APK لأندرويد | Android APK build config
kv/                      # ملفات الواجهة .kv منفصلة | separated .kv UI files
    main.kv
    home.kv
    send.kv
    receive.kv
    settings.kv
app/
    localization.py      # الترجمة عربي/إنجليزي | translations
    network_utils.py     # عنوان IP المحلي | local IP
    settings_store.py    # حفظ الإعدادات | settings persistence
    ftp_server.py        # خادم FTP | FTP server
    ftp_client.py        # عميل الإرسال | upload client
    screens/             # منطق كل تبويب | per-tab logic
assets/fonts/            # ضع خط Cairo هنا | place Cairo font here
```

## التشغيل على الكمبيوتر | Run on desktop

```bash
pip install -r requirements.txt
python main.py
```

> لعرض العربية بشكل صحيح ضع `Cairo-Regular.ttf` داخل `assets/fonts/`.
> For correct Arabic rendering put `Cairo-Regular.ttf` in `assets/fonts/`.

## البناء لأندرويد | Build for Android

```bash
pip install buildozer
buildozer -v android debug
```

## طريقة الاستخدام | How to use

1. شغّل **نقطة الاتصال (Hotspot)** على هاتفك واجعل الطرف الآخر يتصل بها.
   Turn on your phone **Hotspot** and have the other device join it.
2. في تبويب **الخادم** اضغط **تشغيل الخادم** ولاحظ العنوان والمنفذ.
   In the **Server** tab tap **Start Server** and note the IP and port.
3. على الجهاز المرسل، افتح تبويب **إرسال**، أدخل العنوان والمنفذ، اختر الملفات، ثم أرسل.
   On the sending device open **Send**, enter IP and port, pick files, then send.
4. تظهر الملفات المستلمة في تبويب **الملفات**.
   Received files appear in the **Files** tab.
