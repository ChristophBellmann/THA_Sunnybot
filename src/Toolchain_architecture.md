Der Prozess, mit Python code software für mobile Geräte zu schreiben geht folgendermaßen:

Die main.py enthält den Python code, in welchem kivy importiert wird. Diese muss man installieren, und zwar mit:

```
$ python3 -m pip install "kivy[base, media]" kivy_examples
```

In [] benötigen wir base und media, das sind module von kivy. (Media für das kivy4camera Teil).

Nachdem wir das installiert haben, können wir das Setup schonmal testen, und den code auf dem Laptop ausführen.

```
python3 main.py 
```




SunSeeker
see: https://stackoverflow.com/questions/61122285/kivy-camera-application-with-opencv-in-android-shows-black-screen

https://github.com/4ndr3aR/kivy-opencv-demo

https://gist.github.com/ExpandOcean/de261e66949009f44ad2

Toolchain
We need kivy.

```
$ python3 -m pip install "kivy[base, media]" kivy_examples
```
We need adb to test the application on the phone (Android Debug Bridge). Do install:
```
$ sudo apt install adb
```
Not to forget to enable USB Debugging in the system settings on the phone.

optionally: install java if you dont have it:
```
$ sudo apt-get install default-jdk
```

Die Entwicklungsumgebung um für mobile Anwendungen: Kivy
Als Compiler wird benutzt: Buildozer 

https://pypi.org/project/buildozer/


To install buildozer, do:

```
$ python3 -m pip install buildozer
```

For buildozer extra packages are maybe required: 

```
$ sudo apt update
$ sudo apt install openjdk-17-jdk
or more:
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

$ pip3 install --user --upgrade Cython==0.29.33 virtualenv  # the --user should be removed if you do this in a venv
or let decide which version:
$ pip3 install --user --upgrade Cython

```

zeige wo Buildozer liegt: 
```
$ which buildozer
```

It may be necessary to add the buildozer install dir to path:
```
$ export PATH=$PATH:~/.local/bin/
```

INstallation fertig.


Kivy enables the developers to run the application on a desktop machine as well as on the mobile phone.

The command to run the "myapp" test program is: 
```
python3 main.py 
```

Layout is in a seperate file: sunseeker.kv
This kivy file is for user interface.

Now the program needs to be compiled to android.
This needs to happen on a linux machine.

 In the app dircetory create a new dir, so that the only files in there are to be included in the compilatiopn process, there init buildozer
```
$ buildozer init
```
The first run will take a while.

# Run App on the Phone

```
buildozer -v android debug
```

To install the apk, execute
```
buildozer android deploy
```
And to run the App do
```
buildozer android run
```
To create a logfile append this to the start command:
```
 logcat 2>&1 >/dev/null | grep 'python' > filter.out
```

or in a short one-liner:
```
buildozer -v android debug deploy run
```
in case of deploy error, uninstall the app:
```
adb uninstall org.test.sunseeker
```

Debug App on Phone:
```
adb logcat
```
remote connection over adb:
```
adb tcpip 5555
adb shell ip addr show wlan0 # get ip
adb connect ip-address-of-device:5555
```

#to stream the display to a lpatop, use 
#https://android.stackexchange.com/questions/7686/is-there-a-way-to-see-the-devices-screen-live-on-pc-through-adb
```
sudo apt-get install adb ffmpeg    
adb exec-out screenrecord --output-format=h264 - |
   ffplay -framerate 60 -probesize 32 -sync video  -
```
