[app]

# (str) Title of your application
title = SunSeeker

# (str) Package name
package.name = sunseeker

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py file is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) Application versioning
version = 0.8

# (list) Application requirements
requirements = python3,kivy,numpy,opencv,pyjnius

# (list) Supported orientations
orientation = portrait, landscape, portrait-reverse, landscape-reverse

# (str) OS X python version to use
osx.python_version = 3

# (str) OS X kivy version to use
osx.kivy_version = 1.9.1

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions required by the application
android.permissions = android.permission.INTERNET, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE, android.permission.CAMERA, android.permission.WAKE_LOCK

# (list) Android archs
android.archs = arm64-v8a, armeabi-v7a

# (str) The entry point for your application
entrypoint = main.py

# (int) Target Android API to use
android.api = 31

# (int) Minimum Android API to support
android.minapi = 21

# (bool) Enable backup
android.allow_backup = True

# (int) Log level
log_level = 2

# (str) Logcat filters
android.logcat_filters = *:S python:D

# (bool) Warn when running as root
warn_on_root = 1
