# Procedure to get a column of depth values in real time from minecraft on Ubuntu 16.04

## Minecraft installation

1. Download Minecraft through the (Minecraft launcher)[https://launcher.mojang.com/download/Minecraft.deb] (create a free account, this should be enough for our use)

2. Launch minecraft and create a new user profile with version 1.13.2

3. Download (Optifine.jar 1.13.2)[https://optifine.net/downloads] and launch it with `java -jar optifine.jar` command (this should install optifine in your minecraft folder /home/user/.minecraft)

4. Download the Depth map shader (here)[http://www.mediafire.com/file/5tan9hrgjhr3vu4/CPDepthMap.zip] (no need to unzip it)

5. Launch Minecraft and select the optifine profile that has been automatically created

6. Go to options -> video settings -> shaders and select the depth map shader

7. Launch a game, it should be in black and white

## Script requirements

1. Install required Qt libraries by running `pip3 install PyQtChart`. It will auto install "PyQt5" and "PyQt5-sip" that are needed too

2. Given the way the scritp is working for now, you need to open minecraft on place it on the right half of your screen. (this will be changed in the future with detection of minecraft window ID)

3. You might want to change some parameters, the only you should need to change are the 5th ones at the beginning of the script

4. launch the sript with `python3 main.py`

5. Enjoy !

## Script parameters description

this is detailed in main.py file

## Future features

1. Get minecraft windows id and size so it can be displayed anywhere

2. Buttons to change the matrix size directly from the GUI

3. Adjust dynamically the coordinates of the pixels getting read
