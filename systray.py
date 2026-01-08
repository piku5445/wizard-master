import tkinter as tk
from pystray import Icon, Menu, MenuItem
from PIL import Image
import os

imageOFF = Image.open("icons/expOFF.jpg")
turnedON = False
imageON = Image.open("icons/expON.jpg")

def quit_action(icon, item):
    icon.stop()
    os._exit(0)

def switchServer(icon, item):
    global turnedON
    turnedON = not turnedON
    icon.icon = imageON if turnedON else imageOFF

icon = Icon(
    "TrayApp",
    imageOFF,
    menu=Menu(
        MenuItem("Turn off" if turnedON else "Turn On", switchServer),
        MenuItem("Exit", quit_action)
    )
)

icon.run()

