[app]
# (str) Title of your application
title = FileTrasfer

# (str) Package name
package.name = khileshapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.myapp

# (str) Source code where the main.py is located
source.include_exts = py,png,jpg,kv,atlas

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, BILLING, FOREGROUND_SERVICE, INSTALL_REFERRER, com.google.android.finsky.permission.BIND_GET_INSTALL_REFERRER_SERVICE

# (str) The entry point of your application
entrypoint = main.py

# (list) Application requirements
requirements = python3,kivy

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Presplash screen
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) The list of directories to exclude from your application
# (specify as comma separated list)
source.exclude_dirs = tests, bin

# (list) The list of files to exclude from your application
# (specify as comma separated list)
source.exclude_exts = txt, pdf

# (str) Android service to run
#android.service = myservice:MyService

# (str) Android service permissions
#android.service_permissions = 

[buildozer]
# (str) Log level (one of trace, debug, info, warn, error, critical)
log_level = 2

# (int) Number of threads used to compile your app
num_workers = 4

[python]
# (str) Python version to use
version = 3.8

[requirements]
# (list) List of Python modules to install
python_modules = requests, kivy

# (bool) Indicate if the system should install the build requirements
install_build = 1

[android]
# (str) Android NDK version to use
ndk = 21b

# (str) Android SDK version to use
sdk = 29

# (str) Bootstrap to use for the Android build
bootstrap = sdl2

# (str) Android architecture to support
arch = armeabi-v7a, arm64-v8a, x86, x86_64

[build]
# (bool) Indicate if the system should clean the build environment
clean_build = 1
