import time
import win32gui

#Variables
Window = "FINAL FANTASY X"


#Windows manip
def winEnumHandler( hwnd, ctx ):
    global Window
    if win32gui.IsWindowVisible( hwnd ):
        #print(Window)
        #print (hex(hwnd), win32gui.GetWindowText( hwnd ))
        #print(win32gui.GetWindowText( hwnd ).find('Window', 0, 4))
        if win32gui.GetWindowText( hwnd ).find(Window, 0, 20) != -1 :
            print ("Switching windows")
            print (hex(hwnd), win32gui.GetWindowText( hwnd ))
            win32gui.SetForegroundWindow(hwnd)
            
def openFFXwindow():
    win32gui.EnumWindows( winEnumHandler, None )

#Functions
