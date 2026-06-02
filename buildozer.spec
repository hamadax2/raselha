# ─────────────────────────────────────────────────────────────────────────────
#  buildozer.spec  –  FileShare (Kivy 2.2.0 / KivyMD 1.1.1)
#  Target: Android APK via GitHub Actions (ubuntu-22.04, Python 3.10)
# ─────────────────────────────────────────────────────────────────────────────

[app]

# Display name shown on the home screen
title = FileShare

# Internal package identifier (no spaces, no capitals)
package.name = fileshare

# Reverse-DNS domain for the package
package.domain = org.fileshare

# Root of the Python source tree (where main.py lives)
source.dir = .

# Extensions to bundle into the APK
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,ini

# Explicit extra asset folders
source.include_patterns = assets/*,kv/*

# Folders to exclude from the bundle (saves space, speeds compile)
source.exclude_dirs = tests,bin,.buildozer,.git,__pycache__,.github

# App version shown in the store
version = 1.0

# ── Requirements ──────────────────────────────────────────────────────────────
# Rules for this field:
#   • Use "==" pinned versions that have known p4a recipes.
#   • hostpython3 / python3 must match the version that p4a will compile.
#   • kivy and kivymd versions must match exactly what the app imports.
#   • pyftpdlib, arabic_reshaper, python-bidi have no native extensions
#     → they are bundled as pure-Python via the "generic" recipe.
# ─────────────────────────────────────────────────────────────────────────────
requirements = python3==3.9.0,hostpython3==3.9.0,kivy==2.2.0,kivymd==1.1.1,pyftpdlib==1.5.9,arabic_reshaper==3.0.0,python-bidi==0.4.2,plyer==2.1.0

# ── Assets ────────────────────────────────────────────────────────────────────
presplash.filename = %(source.dir)s/assets/splash.jpg
icon.filename      = %(source.dir)s/assets/icon.png

# ── UI ────────────────────────────────────────────────────────────────────────
orientation = portrait
fullscreen  = 0

# ── Android ───────────────────────────────────────────────────────────────────

# Highest stable API with good NDK support in p4a master
android.api    = 33
android.minapi = 21

# NDK r25b is the last version fully supported by the p4a recipes used here
android.ndk = 25b

# Let buildozer auto-download SDK / NDK (required on CI)
android.accept_sdk_license = True
android.skip_update        = False

# Permissions needed by the FTP server + file manager
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# Build only armeabi-v7a for the fastest CI build.
# Add arm64-v8a here if you need a 64-bit slice (doubles build time).
android.archs = armeabi-v7a, arm64-v8a

# Keep auto-backup enabled (harmless for a file-sharing app)
android.allow_backup = True

# Logcat filter – show Python output only
android.logcat_filters = *:S python:D

# ── p4a branch ────────────────────────────────────────────────────────────────
# "master" tracks Kivy's latest p4a; it has recipes for all our deps.
p4a.branch = master

# ─────────────────────────────────────────────────────────────────────────────
[buildozer]

log_level   = 2
warn_on_root = 1
